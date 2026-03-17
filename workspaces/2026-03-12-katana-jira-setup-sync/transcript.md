Mar 12, 2026
Katana: Jira Setup sync - Transcript
00:00:00
 
Alex Del Re: Oh, I'm also on mute. Okay. Uh, I will let you in right now. Sorry, you should be in the meeting. That's good. I assume whenever Lauren joins should be able to hear you.
Lauren Joyce: Morning.
Alex Del Re: Okay. Hey Lauren. Good morning.
Lauren Joyce: Good morning.
Alex Del Re: Uh we'll be talking off of my computer just because uh Mike and I are in the same room, but uh he's here, trust me.
Lauren Joyce: I believed
Alex Del Re: Um yeah.
Lauren Joyce: it.
Alex Del Re: Yeah. So I I uh thanks for joining. Today I think will be more of like a working level session. Um Mike had some questions on the Jira space um which we will try and tackle with either me or you. I assume because you have admin capabilities you can maybe add him to things that I can't and then um assuming you can't add him to something.
Lauren Joyce: Yeah.
Alex Del Re: We'll um well what do you call it?
 
 
00:01:16
 
Alex Del Re: Um file IT tickets or something like that.
Lauren Joyce: Yeah. Sounds good to
Alex Del Re: So um yeah.
Lauren Joyce: me.
Alex Del Re: So I guess Mike, let's start off. I know like the first thing you wanted to tackle creating was like a project board on on uh this the kind of space. You wanted to have something catered specifically for um software development um maybe expand upon that or Yeah. Yeah. just I guess being able to create one of our own boards, being able to run the filters that go along with that kind of break our
Lauren Joyce: Good morning.
Alex Del Re: work out separately than applied side. Okay. And I guess the whole I guess the push behind this would be uh I assume as we get into this, our workload is going to grow rapidly with the amount of tickets we're trying to put in and just trying to bring you guys in on all that is just going to be way too much trying to, you know, get your help with everything and so on.
 
 
00:02:21
 
Alex Del Re: Okay. Um in my mind, what this seems to me is like we can start by looking at this filter. Um so this is all the current tasks in um that uh software STV top level initiative. So we can kind of grab all the task using this guy right here and then kind of break it out into like kamasu specific users. So right now it's pretty narrow in scope because there's only like six of you guys or four four six whatever. So we can just be like and user is so and so on and so forth. Um, what is it? Assige. Yeah. So, assigne in. Sorry, I'm not very familiar with SQL.
Lauren Joyce: No, no, no. Jool, this is this is good.
Alex Del Re: Uh, and then I guess I can just do in how do you do like a list in this? I have no idea.
Lauren Joyce: Um,
Alex Del Re: Uh,
Lauren Joyce: I think you do like comma separation,
 
 
00:03:19
 
Alex Del Re: but I'll do Okay.
Lauren Joyce: but it's okay.
Alex Del Re: So,
Lauren Joyce: You can just Yeah. try to add
Alex Del Re: I'll do Mike. Uh,
Lauren Joyce: people.
Alex Del Re: oh, Michael is probably you. Michael Lamb. Oh, maybe Lamb. There you go.
Lauren Joyce: Ah,
Alex Del Re: Michael Lamb.
Lauren Joyce: okay.
Alex Del Re: All right, perfect. I think that's it. So, then Joseph Ber. Oh, because you can't do spaces. That's fun.
Lauren Joyce: Yeah.
Alex Del Re: uh Jonas. So, I guess do you get what I'm trying to do here? Like create a list and then uh we can use that to influence a board after this, right? Yeah. Is that kind of what you're looking for? Or something different? Sort of.
Lauren Joyce: I think
Alex Del Re: Um and maybe maybe I'm just not seeing I guess maybe you guys use this differently than I've used it in the past.
 
 
00:04:11
 
Alex Del Re: Um I So it looks like we've got the uh epic at 1760 that would be holding our work. I guess I'm a little more familiar with using an epic as more of like a a deliverable feature that would close out with a release rather than like a permanent holding ground. I mean having a few as a permanent holding ground for you know uh I think there's one in there for like Jira workflow thing. I can't remember exactly what it's called, but having a few of those makes sense. But like a forever effort to dump everything in just seems like wouldn't have I don't know.
Lauren Joyce: Yeah.
Alex Del Re: I'm just not familiar with using it that way. Yeah. So the kata 1760 I I'll show you like how we organize the work and that might make clear. Um Oh, don't go to the board. I I'll just show you the plans page because I don't know actually how to quickly show you all the the top level initiatives but like as you know we have this whole entire katana works katana engagement that has all these work streams that compose comprise it um the that is what is organized into top level initiatives.
 
 
00:05:25
 
Alex Del Re: So like surround view system that will have associated epics and each one of those epics will kind of be related to a specific feature or like large scale development for that workstream. So for uh software defined software or I say software defined software software defined vehicle um this is what we are looking to do for you guys and there's like a few different uh epics we're thinking about here. they're going to be um kind of planning uh core vehicle OS development from applied um and then ignore like these next four because or ignore the exterior lighting stuff because we're building out what it's going to look like next. But moving forward,
Lauren Joyce: Hey,
Alex Del Re: we're going to have an epic for each one of the apps that you guys are going to be working on. So like one for autoloop, one for payload, hoist, brakes, steering, all so on and so forth. Um and anything like that is needed to supplement those will be kind of encapsulated in that epic but general work that whether it's you know OTAA that applies to all or specific diagnostics buildouts or anything that's like general across the platform will be its own epic.
 
 
00:06:32
 
Alex Del Re: So the uh kind of the schema here is like we have some features some some some feature and then we have subtasks that kind of characterize the the work there. Yeah. I think generally that makes sense. I would maybe break the autoloop application stuff down into smaller ethics than that. Um just so you can like maybe there's one for requirements that can be closed out. I'm I'm thinking in terms of like in in releases um you'd want to try to get an epic closed versus like auto lube development just sounds like something that'll go on for six months or something like that. Sure. Can you do sub epics? I don't think you can. Yeah, that'd be that'd be extremely useful. But like I hear what you're saying there, but the idea is like maybe Lauren, you have something to say on this, but like we shouldn't be afraid to create a lot of tasks for a given um given epic. So like let's say auto loop is going to have like a bunch of different work requirements, development, testing.
 
 
00:07:36
 
Alex Del Re: Um there's probably things we can do within those individual tests themselves. maybe some labels or some naming convention to say this is a requirements thing and then from there we can take a filter and have specific dedicated views for a given epic and like the subtask related to a domain. Does that make sense? Yeah. Like and it will be cluttered in like this view um like we see here but uh it would be we could like pick and choose what we want to see in this case. Yeah. So I've I've done that before um years ago where I used like we want to develop an accelerator subsystems. So we made an accelerator epic and that accelerator epic basically lived through a majority of the project and then we dumped all of our tickets into that and it basically just becomes a bucket that never closes. Um, and then for your we got John and Lee or whatever for like stakeholder level Josh whatever like those higher level guys that aren't in the development every day.
 
 
00:08:42
 
Alex Del Re: That's kind of where they would view things like at an ethic level like this is the feature we're trying to deliver on this time frame. They don't care about the junk that's inside of it. Um, it just kind of gives you that ability to break the work up that way into smaller deliverables, I guess. Yeah. Yeah. Yeah. Um, so that would be, I guess, one of the goals of mine would be to kind of be able to break things up like that. Um, yeah, that is a good point. I mean, like, if we just have this open Epic for six months or two two releases while we're working on auto loop or something like that, that doesn't look great. I think I don't know like how we do it is like very much framed in the steer co arguments of like this is what we're focus focusing on for that this release and thinking about it in terms of are we closing this epic or whatnot shouldn't be like the yard stick in which we measure um for like for leadership like how we're trying to define success for katana for software is like we we align on these x goals for uh this year co for the upcoming release and did we accomplish those or not.
 
 
00:09:51
 
Lauren Joyce: Good
Alex Del Re: And kind of like how do you see that you've accomplished them?
Lauren Joyce: morning.
Alex Del Re: Uh how do we see that we've accomplished them? Like if you close an epic that's open for multiple months or whatever, what what is being completed? I guess is it just the individual tickets? So I can talk about tool chain because like we've gone through a couple releases there on um uh what do you call it on like working on the uh the platform. So the virtual tool chain that you can see here um we can see like there's a few different epics we have beneath and these these are like correspond to like overarching goals we want to release do for a given steer code. So one of the um tasks for the last steer code was to have a kamasu repo built out um and have the ability for uh like kamasu devs to download it to their machines. So that kind of fell under this dei de developer environment setup. Um and while this epic this has been open for like eight months at this point or six months at this point this specific epic I've been adding and uh adding tasks underneath.
 
 
00:10:55
 
Alex Del Re: I don't know if you can see all the done tasks but like all the tasks underneath that like we've completed and to say like whether or not we're done or not for this specific for that steer code goal. It's about demonstrating it with Kamasu users and then showing that during showcases and then um uh what do you call it? Uh talking about it during steer code. I guess Lauren, do you have any like insight into how we present the work that is done for a given steer code to Kamasu
Lauren Joyce: Yeah,
Alex Del Re: leadership?
Lauren Joyce: I feel like typically the the barometer for like whether or not we've made progress like has to do with the showcase. Like if we can physically or like somehow in simulation show that we were able to develop like the feature or capability that was promised at the beginning of steer code. That is typically like the biggest not being able to check that box. Um, Mike, I kind of I'm aligned with you of like there there's a more compelling argument for like being able to measure things getting completed.
 
 
00:11:52
 
Lauren Joyce: Um, as well, I think that this release is a little bit trickier just because a lot of the work is like very planning related, but I think for Q2 there's going to be a lot of like tangible deliverables um both on the software and the hardware side. So, it makes more sense to align that with actually being able to close things out in Jira. Um, I think the thing that I want to say when it comes to like Jira and like your usage and our usage is that like this is just like how we do it. Um, and I don't see like uh like your usage needing to necessarily fit into that mold. Like I think obviously having some base level of alignment there is good, but as the person who's managing the space, I like don't like have an issue with you kind of running your section like how you want to. I think there's a world in which like we um create maybe a distinct top level initiative for like just application software development or like whatever you guys are doing and then anything that sits under that like you can make as many you know again like epics as you want or tasks or if you want us to add like the story type because it's easier for you to keep track there's lots of things that we can do there.
 
 
00:12:54
 
Lauren Joyce: Um so yeah I think like view this is just like us walking you through how we organize things so far and then um you can get creative on like how you want to nest within this structure. Um because Alex is right like we can use filter view to kind of pull everything like for your teams but if it's all better like in one place or even yeah a top level initiative for autoloop for example then suddenly you can break that down into like different work streams of how you guys think through it. Um because this is all internal like no one's going to look at this and be like why is it all seven work streams and then auto loop. Um no one really cares except for me and and I don't. So does that like sort of like maybe help frame it a little bit more? I just want to yeah emphasize that um I don't mean to box you in in any way.
Alex Del Re: No. Yeah, that's that sounds pretty good. Um, I guess I think from our team's side,
 
 
00:13:39
 
Lauren Joyce: Okay.
Alex Del Re: I think I'm probably the only one with Jura experience. Um, so I I guess I guess see myself as the the leader for the team in that regard. Um, and I I know how quickly the task load can blow up as you start getting into a program. Um, and I just I don't want to get into a spot where we're like having to rely on you guys, you know, several hours a day like, hey, we need this ticket or hey, is this in the right spot or like I can kind of help the team through that.
Lauren Joyce: Yeah.
Alex Del Re: So, um, certainly kind of picking up some of the things you guys have done. I'm open to learning things. That's great. Mhm. Um, so I mean it sounds sounds good. Sounds like we can work together on this. Um, so yeah.
Lauren Joyce: Yeah.
Alex Del Re: Yeah.
Lauren Joyce: And
Alex Del Re: Personally, I was even aware we could add top level initiatives.
 
 
00:14:30
 
Lauren Joyce: I
Alex Del Re: So if we want to be if we want to add them, let's do it. Like let's just go for it. Yeah. I don't even have the access to initiatives in my last job,
Lauren Joyce: Yeah.
Alex Del Re: but um yeah, I guess that's more better.
Lauren Joyce: Yeah.
Alex Del Re: Just making sure you like these.
Lauren Joyce: It's worth No,
Alex Del Re: Oh, go ahead, Lauren. Sorry.
Lauren Joyce: I was just going to say I was just going to say exactly what you're going to say, which is it's worth verifying that you have all these permissions um of like you being able to to create them and then I can unblock you in terms of like if it won't allow you to make certain kinds of issues or certain kinds of actions, just let me know um and I can add those. But yeah, I mean go crazy like
Alex Del Re: Yeah,
Lauren Joyce: Yeah.
Alex Del Re: the ones I mean the ones I've run into so far I think are just listed in that message.
 
 
00:15:12
 
Alex Del Re: Um,
Lauren Joyce: Yeah. Um, let me take look through that really quick.
Alex Del Re: thanks Mike.
Lauren Joyce: Um,
Alex Del Re: I just sent a link in the uh Google chat. Are you able to open that page? just internet.
Lauren Joyce: uh,
Alex Del Re: Is this is it the meeting chat or is it is the meeting chat but I'll send it to you on Slack just so it's more persistent. Oh,
Lauren Joyce: Oh,
Alex Del Re: that's not red.
Lauren Joyce: here we go.
Alex Del Re: But here we
Lauren Joyce: um creating sprints. Yeah,
Alex Del Re: go.
Lauren Joyce: so sprint creation is is a little bit tricky. Um just because we don't use the built-in sprint feature in Jira. Um this kind of relates to what I was talking about before of like we use custom fields so that we can port tickets between different instances that applied. Um I as far as creating releases goes um yeah I don't think you have permission to do that.
 
 
00:16:09
 
Lauren Joyce: you don't use again the release feature that's built into Jira as well. That said, um I'm actually meeting with like our our lead TPM um like at Applied about adding releases to the Katana space. So, I can keep you posted on that on Friday, which I guess is tomorrow. Um plan view is maybe something worth us tackling uh today as well as boards. I'm surprised that you don't have permissions to do that. So, let me either get grant you permission to do that or we can work through one together. I think I would just rather grant it to you. Um, and then modifying the tabs at the top of the space that I actually haven't tried, so it's worth trying that.
Alex Del Re: Yeah.
Lauren Joyce: Um,
Alex Del Re: Over over on the right side where I think where it says more it there's usually like a three
Lauren Joyce: sorry.
Alex Del Re: dots or something up there and then you can go and pick and choose what shows up there. The the other side of this is I think previously uh my last job I had almost like top level rights.
 
 
00:17:05
 
Alex Del Re: It was almost a little scary. It's like I could get in and manipulate like everything and now I'm on the complete opposite side of it. So it's like I don't know I guess where the middle ground is of what normally have.
Lauren Joyce: Totally.
Alex Del Re: Uh yeah, I mean like unfortunat I don't know if do we have like a Jira admin on the Kamasu side, Lauren? Maybe we can make Mike.
Lauren Joyce: Um yeah,
Alex Del Re: I don't know if like we want to do that, but
Lauren Joyce: I mean we um let me ask Greg.
Alex Del Re: yeah.
Lauren Joyce: I think it would be advisable to have one. Uh and yeah, I think the right person would be Mike for sure. So, um, here I'm gonna take over really quick if that's cool and just share my screen.
Alex Del Re: Yeah.
Lauren Joyce: Um, so Mike, when you say the the things at the top, um, do you mean these here? Like, um, these guys.
Alex Del Re: Yeah, all works code.
 
 
00:17:55
 
Alex Del Re: Yeah,
Lauren Joyce: Okay.
Alex Del Re: there's a way that you can manipulate those because like they
Lauren Joyce: Um, I'm trying to
Alex Del Re: have used
Lauren Joyce: um, let's see. Uh, not off the top of my head, but let's see. Board settings. Um, I guess here's all the administrators. I don't know who Andrew Pierce is, if anyone does, but yeah,
Alex Del Re: Uh, I think he's an IT
Lauren Joyce: let me Oh, that feels right. Oh, columns.
Alex Del Re: guy.
Lauren Joyce: Um, yeah, let me um let me take a look at this later. Mike, I'm just not sure how it works. Um, so I'll make a note of that. Um, in terms of plan creation, yeah, I think that what makes the most sense, and let me just ask Greg about this, is giving you permission to do all these things, having you kind of build out what you think would work the best or like what you have historically used and then us going through it together and just like making sure everything checks out.
 
 
00:18:58
 
Lauren Joyce: Um, I think that's maybe the best path forward instead of like you translating what you want through me, me me trying to make it and then us iterating on it with your like and you unable to actually like get hands-on and do it. Um, so let me let me check on that. I'm not sure like what the permissions layers actually look like um of like what makes um you know a member different than an admin different than a manager and stuff like that. So um I think that that's worth looking into permissions wise for me. Also quickly um just because I'm looking at it right now um story points aren't relevant for Kamasu's side of things. Um story points are only used for apply to like manage um or I guess like measure the contractual amount of effort that we put towards things on behalf of Kamatsu. It's like sort of outlined in the the partnership. Um so it's only used to manage applied effort. If you similarly want like something similar to like I don't know approximate how long a task will take.
 
 
00:19:53
 
Lauren Joyce: There should be an effort field. Um and if there's not I can add it. It just depends on like what you want for that. Um but I don't know. It's only if you want it. Yeah. But just wanted to clarify the story points are only for the applied side.
Alex Del Re: Okay. Yeah, I've I haven't really been big into story points. It just seems like a lot of planning and estimating for things to not be right anyway.
Lauren Joyce: Right.
Alex Del Re: But that's just my um so yeah.
Lauren Joyce: Yeah. Just don't worry about story points on your
Alex Del Re: I'm not too worried about story points.
Lauren Joyce: guys.
Alex Del Re: The sprints I'm kind of okay with. I mean, they're builtin boards are kind of nice to have. It's just it's a really easy way to see backlog stuff. Um, I don't know if that comes with the boards feature that we were talking about. So, maybe they come together.
 
 
00:20:41
 
Alex Del Re: I'm not sure. Well, I guess we'll
Lauren Joyce: Yeah,
Alex Del Re: see.
Lauren Joyce: the way that we look at it right now is like we have filters that are always set to like the current and previous sprint and then that's how we're always filtering sprints wise. Um I don't see us being able to use the sprint board anytime soon just because the um sprint v2 custom field is like the source of truth across all of applied. Um, so I would maybe not not go for that. Releases is like on my agenda and then yeah, getting you permission for boards and things like
Alex Del Re: So yeah, I guess on the sprint side,
Lauren Joyce: that.
Alex Del Re: um are we you're saying we wouldn't be able to use it even in our own space because it would affect the way you guys use it?
Lauren Joyce: Um, not necessarily. I think it would just require us to track like two sprint fields separately because right now like the way that we track sprints is through that custom field.
 
 
00:21:36
 
Lauren Joyce: So we're not actually tracking the sprints like in Jira. So in order for things to track correctly in your sprint board, you would have to specify the applied sprint and like the Jira sprint for it. Um which is just sort of like it makes it a bit messy. if you're like confident that like you can get your your people to do that or if you specifically want to do that of like tagging two release or sorry two sprint fields um in order for them to get tracked correctly on the sprint board that's your prerogative.
Alex Del Re: Would
Lauren Joyce: Um but we just need to make sure that it gets tracked um at least in the applied sprints if not both.
Alex Del Re: you would you be tracking sto like sprints and well probably not the story points but would you be tracking the sprints on power
Lauren Joyce: Um, it's a good question. I think like adjacently, yes. Um, if there's ever dependencies like with, I don't know, steer code milestones or the lab truck and things like that, it's good to keep a pulse on it because they're all in the same space.
 
 
00:22:40
 
Lauren Joyce: The field is going to be there no matter what. I guess whether or not you fill it out is sort of up to you. I guess Alex then that becomes sort of a question of like what is the nature of like Kamatsu's tickets in this case? Like are we converging closer towards collaboration further away? Like how much work will we on the applied side need to do with the work that's getting tracked in these tickets? cuz yeah, I think that that's maybe what I don't understand at the moment because all of the work that we've been doing so far has been very interwoven, but it sounds like once we get um trucks team on their feet, they'll be able to do application development pretty independently. So don't understand like where the convergence happens in
Alex Del Re: Yeah.
Lauren Joyce: there.
Alex Del Re: I mean like the expectation now is that we're going to be working very closely together on like getting making on making sure you guys can develop on our platform but you know fast forward six months a year down the line like you guys are going to be pretty much self-sufficient when it comes to actually writing the code and if we want to have that tracked in our shared space or if you guys have an internal place you want to track
 
 
00:23:42
 
Alex Del Re: it that's kind of like whatever works best for your team but um yeah I'd say the the end goal is that you guys are going to be kind of developing on your own and then when you have feature requests for the plat for the vehicle west platform or whatever else that applied you need specific applied help on that's like where we'll have uh more input on the ticket or the task but yeah does that make sense? Yeah.
Lauren Joyce: Yeah,
Alex Del Re: Yeah.
Lauren Joyce: cuz then Oh,
Alex Del Re: I guess that it brings up a bigger question of like are we I
Lauren Joyce: go ahead.
Alex Del Re: see I see Jira and I'm like I'm jumping on it because I'm just used to it and like oh this is great. we can use this to track everything. Uh long term, are we going to be using Jira or are we just supposed to bring that stuff internally and track our own work? Like, you know, with issues that don't involve you guys and and whatnot like do we need to be using Jira?
 
 
00:24:37
 
Alex Del Re: Is Jira going to be available to us in two or three years? so on. Um, that's probably a bigger question to answer as well. Yeah,
Lauren Joyce: Yeah.
Alex Del Re: I think this is a good question for like Jeff and Lee and John to not but Jeff and Lee to talk
Lauren Joyce: Yeah.
Alex Del Re: about I would say like figure out what makes the most sense later down the line. As far as I know, like during the lifetime of the applied katana or kamasu like engagement, you'll have access to all these tools because like we provide them as part of the work that we do together, but Okay. Yeah. Yeah. We'll just run with it for now then. Yeah.
Lauren Joyce: So Mike, do you guys use Jira internally or how are you task tracking at
Alex Del Re: Maybe we can get they used
Lauren Joyce: Kamatsu?
Alex Del Re: uh DevOps. Um and I I just I just started in Kamasu in
 
 
00:25:19
 
Lauren Joyce: Oh, like Microsoft.
Alex Del Re: January. Um so I I didn't even get a chance to get into DevOps.
Lauren Joyce: Okay.
Alex Del Re: I don't know how it runs and how it works.
Lauren Joyce: Gotcha. Yeah. Because my my thing was like, oh, like should we have like, you know, you guys working out of the the Kamasu Jira space, but that doesn't exist. Um, I'm realizing. So, um, okay.
Alex Del Re: I'd love to,
Lauren Joyce: Yeah. Right. Make it easier.
Alex Del Re: but
Lauren Joyce: Yeah, understood. Um, and then, okay, two quick things I wanted to hit just because I saw you noted them, um, in this message as well. Removing the release requirement from new ticket entries. Um, I'm I'm still inclined to keep that just because um, if we're breaking stuff into like three month blocks, ideally, like we should be able to map it out that far and move it around if it becomes not relevant. Um I think the reason that it mostly is required is because on the applied side like in the near term sometimes people forget to put it and then we end up not being able to actually track all the work appropriately um release over release.
 
 
00:26:26
 
Lauren Joyce: If it becomes an issue where you're scoping tasks too far in advance for the amount of releases that we have available like for example you want to scope something for 26.3 or 27.1 and we don't have that yet. Um I can add those fields for you um or just like put them yeah far in advance. But I'm hopeful that tasks wise we should be able to assign things on like a quarterly basis and then move them pretty easily that way. Um, does that sound okay with you?
Alex Del Re: the on the like on the task side and bug side of things. I I have concerns about that field on in terms of like epics and creating those like we want to make a I mean right now with the auto but like whatever the next subsystem is or the next couple like those should be I think fairly easy to kind of drop into a release from the get-go. Um it's just like those day-to-day issues you come across and that oh we don't want to lose track of that but we have no idea when we're going to work on it or it doesn't quite make sense to me
 
 
00:27:28
 
Lauren Joyce: Okay. Um, yeah. Let's Yeah. Yeah. Go
Alex Del Re: this more complicated on the back end here's how how
Lauren Joyce: ahead.
Alex Del Re: how much appetite I guess there is to do any of this but I mean Jur provides a way to make different issue types and issue schemes. Um, and then you can select the fields and and workflows and all that thing all those different settings for those.
Lauren Joyce: Yeah.
Alex Del Re: So like maybe come up your own
Lauren Joyce: I mean that could
Alex Del Re: schemes.
Lauren Joyce: be Yeah. I don't know. Do you mean like your top level initiative could have different like field settings than the rest of
Alex Del Re: Um,
Lauren Joyce: them?
Alex Del Re: it's a little bit deeper in Jira than that. So like your you basically have like your your task and your bug and your
Lauren Joyce: Yeah. Yeah. Yeah.
Alex Del Re: epic and your story like two types you can set up a different scheme with like a different name and it's all its own like what fields are required on entry, what fields show up when you're just looking at it.
 
 
00:28:38
 
Alex Del Re: Um what what kind of
Lauren Joyce: Yeah, I mean we could we could get it to a place where like release is only required when something is moved to in
Alex Del Re: transition?
Lauren Joyce: progress or something is moved from backlog to to-do. Like maybe that's worth pursuing. Okay, let me look into that.
Alex Del Re: Yeah.
Lauren Joyce: Um.
Alex Del Re: Yeah.
Lauren Joyce: Um. Okay, cool. Yeah, I think that that's you
Alex Del Re: I'm not guess I'm eager to jump on that just because I know it is it's
Lauren Joyce: got
Alex Del Re: days worth of work to get that stuff set up. It's a lot of back and forth,
Lauren Joyce: it kind of random. I know.
Alex Del Re: but it's an option.
Lauren Joyce: Um, yeah. No,
Alex Del Re: Yeah,
Lauren Joyce: let me look into that. I think Yeah,
Alex Del Re: I mean like No,
Lauren Joyce: go ahead.
Alex Del Re: I was going to say like it is a lot of work.
 
 
00:29:21
 
Alex Del Re: It was a lot of work, but I don't know. Like Lauren, you just created like a pretty slick new like uh MCP for Jira with uh kind of like automatically create tickets. I'm sure the MCP has some sort of context on how to like set up a workflow. And if it doesn't, maybe we can kind of like, you know, cursor it around. So, it's like not a unworthy exercise to explore,
Lauren Joyce: Yeah,
Alex Del Re: I'd say. I'm curious.
Lauren Joyce: it's something that I'll I'll throw on my on my list for sure.
Alex Del Re: I can show you after this.
Lauren Joyce: Yeah.
Alex Del Re: Yeah.
Lauren Joyce: Um,
Alex Del Re: Yes. Oh,
Lauren Joyce: and then,
Alex Del Re: sorry.
Lauren Joyce: oh, no, all good. All good.
Alex Del Re: Yeah.
Lauren Joyce: Um, I just know we're at time and I have to jump right now, but last thing is adding the story issue type. Um, we we just don't have it right now.
 
 
00:30:01
 
Lauren Joyce: Do you feel like there is like do you feel strongly about having it as like another layer in the hierarchy? The only thing I want to avoid is just like adding a new issue type and then applied being confused about it. Um, if if there's not like a huge value ad, if like you feel like it would be of significant value to have this additional type that we don't currently have, I think it could be worth looking into. But I just want to understand like the desire for that versus like, oh, it's just like what you're used to. Is it like something that we should consider adopting at a bite in general? Uh, yeah. I just want to understand
Alex Del Re: Yeah, we put a lot of we built hooks around the story and bug types before um and we left the task types as like you know comments, documentation, whatever like planning whatever type of work you want to do and then those the hooks around the we got to run the the hooks around the the story and plugs were really around like release notes and things like that. So like we could ensure that you're going to hand things off
Lauren Joyce: Yeah. Yeah.
Alex Del Re: properly. Yep. Yeah. What I'll do is I'll share notes about this then we can continue the conversation later. All right.
 
 
Transcription ended after 00:32:32

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
ting
