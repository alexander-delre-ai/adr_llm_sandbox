// Package onboarding implements the /katana-onboard Slack command, which files
// Komatsu engineer onboarding requests in Jira Service Management. It is the Go
// port of scripts/katana_onboarding (the onboard and slack-add subcommands).
package onboarding

import (
	"context"
	"fmt"
	"strings"

	"slack-go/eventlog"

	"github.com/slack-go/slack"
	"go.apps.applied.dev/lib/slacklib"
	"go.uber.org/zap"
)

// Modal callback IDs and form block/action IDs. ViewSubmission handlers and
// GetValue both key off these, so the modal builders and the handlers must agree.
const (
	onboardModalCallback  = "katana_onboard_new"
	slackAddModalCallback = "katana_onboard_slack_add"

	blockEngineers  = "engineers_block"
	actionEngineers = "engineers_input"
	blockLocation   = "location_block"
	actionLocation  = "location_select"
	blockPriority   = "priority_block"
	actionPriority  = "priority_select"
	blockChannels   = "channels_block"
	actionChannels  = "channels_input"
)

// Register loads the Atlassian credentials and wires up the /katana-onboard
// command and its modal submission handlers. It returns an error if the
// credentials cannot be loaded, in which case no handlers are registered.
func Register(ctx context.Context, bot *slacklib.Bot) error {
	c, err := loadCreds(ctx)
	if err != nil {
		return err
	}
	registerHandlers(bot, c)
	return nil
}

func registerHandlers(bot *slacklib.Bot, c creds) {
	bot.Command("/katana-onboard", func(ctx *slacklib.CommandContext) {
		sub := ""
		if fields := strings.Fields(ctx.Text); len(fields) > 0 {
			sub = strings.ToLower(fields[0])
		}
		eventlog.Add("slash_command", ctx.UserID, ctx.ChannelID, "/katana-onboard "+sub)

		switch sub {
		case "new":
			if err := openView(bot, ctx.Context(), ctx.TriggerID, buildOnboardModal()); err != nil {
				zap.L().Error("failed to open onboard modal", zap.Error(err))
			}
		case "slack-add":
			if err := openView(bot, ctx.Context(), ctx.TriggerID, buildSlackAddModal()); err != nil {
				zap.L().Error("failed to open slack-add modal", zap.Error(err))
			}
		default:
			ctx.Reply("*Katana onboarding*\n" +
				"• `/katana-onboard new` - file the Okta + Slack provisioning ticket for new engineers\n" +
				"• `/katana-onboard slack-add` - add engineers to additional Slack channels")
		}
	})

	bot.ViewSubmission(onboardModalCallback, func(ctx *slacklib.ViewContext) {
		userID := ctx.UserID
		engineers, err := parseEngineers(ctx.GetValue(blockEngineers, actionEngineers))
		if err != nil {
			notify(bot, userID, "Could not file the onboarding ticket: "+err.Error())
			return
		}
		location := ctx.GetValue(blockLocation, actionLocation)
		priority := ctx.GetValue(blockPriority, actionPriority)
		eventlog.Add("katana_onboard", userID, "", fmt.Sprintf("%d engineer(s), %s/%s", len(engineers), location, priority))

		// Jira call is slower than Slack's 3s window: do it in the background
		// and DM the result.
		go func() {
			link, err := createOnboardRequest(c, engineers, location, priority)
			if err != nil {
				zap.L().Error("onboard request failed", zap.Error(err))
				notify(bot, userID, "Onboarding ticket failed: "+err.Error())
				return
			}
			notify(bot, userID, fmt.Sprintf("Onboarding ticket created for %d engineer(s): %s", len(engineers), link))
		}()
	})

	bot.ViewSubmission(slackAddModalCallback, func(ctx *slacklib.ViewContext) {
		userID := ctx.UserID
		engineers, err := parseEngineers(ctx.GetValue(blockEngineers, actionEngineers))
		if err != nil {
			notify(bot, userID, "Could not file the Slack channel request: "+err.Error())
			return
		}
		channels := parseChannels(ctx.GetValue(blockChannels, actionChannels))
		if len(channels) == 0 {
			notify(bot, userID, "Could not file the Slack channel request: no channels provided")
			return
		}
		eventlog.Add("katana_slack_add", userID, "", fmt.Sprintf("%d engineer(s) -> %s", len(engineers), strings.Join(channels, ", ")))

		go func() {
			link, err := createSlackAddRequest(c, engineers, channels, defaultLocation, defaultPriority)
			if err != nil {
				zap.L().Error("slack-add request failed", zap.Error(err))
				notify(bot, userID, "Slack channel request failed: "+err.Error())
				return
			}
			notify(bot, userID, fmt.Sprintf("Slack channel request created for %d engineer(s): %s", len(engineers), link))
		}()
	})
}

// notify DMs the user with a result. Uses context.Background() because it runs
// in a goroutine after the request that triggered it has returned.
func notify(bot *slacklib.Bot, userID, text string) {
	if _, err := bot.SendDM(context.Background(), userID, text); err != nil {
		zap.L().Error("failed to send result DM", zap.Error(err))
	}
}

func parseChannels(raw string) []string {
	var channels []string
	for _, c := range strings.Split(raw, ",") {
		if c = strings.TrimSpace(c); c != "" {
			channels = append(channels, c)
		}
	}
	return channels
}

// openView opens a modal built as a raw slack.ModalViewRequest. slacklib's
// modal builder does not expose initial values, so we build views directly to
// support prefilled fields and default-selected options.
func openView(bot *slacklib.Bot, ctx context.Context, triggerID string, view slack.ModalViewRequest) error {
	client, err := bot.Client()
	if err != nil {
		return err
	}
	_, err = client.OpenViewContext(ctx, triggerID, view)
	return err
}
