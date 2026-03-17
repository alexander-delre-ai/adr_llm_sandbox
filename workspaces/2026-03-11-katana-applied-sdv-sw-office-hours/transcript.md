Mar 11, 2026
Katana <> Applied: SDV SW Office Hours - Transcript
00:00:00
 
Alex Del Re: Hey, Mike.
Mike Lemm: Hey.
Alex Del Re: Uh, I think you saw that PR got merged in for CMO. I'm not sure if you've been able to access workbench yet.
Mike Lemm: Yeah, I I merged it.
Alex Del Re: Yeah.
Mike Lemm: I pulled it in. I'm working through trying to make some new stuff work. So, seems to be not complaining anymore. Thank you,
Alex Del Re: Cool. This is This is just It's weird. Like, I know you guys are so close, but we're in a meeting together. Uh Oh,
Mike Lemm: Welcome to the on-site remote
Alex Del Re: yeah. Oh,
Mike Lemm: meeting.
Alex Del Re: yeah. Um yeah, there there's going to be someone else from Apply joining. Ashley has to miss today. Um she has an appointment she can't miss. But um Timothy from Applied, he's a new member of my team. He's going to be joining the Kamasu account. So I'm just going to have him kind of shadow office hours moving forward and kind of get a lay of the land as like what's going on with STB development.
 
 
00:02:02
 
Alex Del Re: But um yeah, just while we're waiting for him um I I got some feedback from John Osborne about uh stronger or I guess before I go into this topic, is there anything from the Kamasu side that people want to talk about? Okay. Um, I got this topic I was telling Joe about from John Osborne. Um, just I think him and Lee are looking for a bit more clarity in terms of Jira about like what uh development has been going on. So uh from the Kamasu side. So um looking at uh the top level initiative we have in Jira for software um I'm going to be working on adding in epics for each one of the managers that your team is going to be working on developing and um beyond these or below these there's there's going to be subtasks for they're not in here yet but um things like requirements definition subsystem modeling state machine development functional uh performance requirements, all like the kind of nitty-gritty we need to lay out for the the work up ahead of us, up ahead for us.
 
 
00:03:28
 
Alex Del Re: Um so I just wanted to put that on your team's radar as uh a lot of tickets will be getting created and not clear to me exactly how they're going to get assigned, but um you may see some more stuff in here. Um, and also like if there's anything specific to like auto loop or the app that you're going to be working on, okay, don't hesitate to file a ticket in in the respective space. Um, any questions from the Kamasu team on that?
Mike Lemm: Yeah, I I'd like to kind of get in on some of that,
Alex Del Re: I'd like to get in
Mike Lemm: but I don't have, I guess, access at this time to help draw any of that up. Um, or at least use some of the tools that are built in there.
Alex Del Re: So, when you say you're missing access, do you mean you're unable to make these epics or something
Mike Lemm: Uh, the like the plans feature. I think that would be a really nice one to be able to see. um just any we can't create anything.
 
 
00:04:28
 
Mike Lemm: Can't create sprints, plans, boards, releases. Everything's pretty much locked out. I think the only thing we can do right now is make tickets.
Alex Del Re: I see. Okay. Like so like you're saying Mike you would want more access for you know like going to this page and defining from like the planning perspective.
Mike Lemm: Yeah, I think that's probably what John and Lee would probably want to see.
Alex Del Re: Yeah.
Mike Lemm: Um, something like that rather than just a pile of tickets.
Alex Del Re: Yeah. Um, I mean like from my perspective, we can talk about this uh outside of office hours. It's not really directly related to, you know, the software development,
Mike Lemm: Sure.
Alex Del Re: but like um I've been using the plans page a lot for like ticket drafting um as a way to like kind of draft them before they become set in stone or or set into reality. Uh maybe you can share some learnings with me on like how to best use this page um to kind of plan out app development.
 
 
00:05:27
 
Alex Del Re: Um, in a parallel note, we talked about this with Lauren in terms of like getting you guys access to like updating this page. Um, or maybe a plans page. I'm pretty sure like we can create a new one for y'all or I forget. Yeah, like here or something like that that you guys can work with.
Mike Lemm: Sure.
Alex Del Re: Maybe that's a workaround we can we can look to explore. But um, yeah, I know Lauren is looking into it with this. So I'll I'll bumper on that after today.
Mike Lemm: Okay. Yeah, cool. I'm I'm open to whatever.
Alex Del Re: Yeah.
Mike Lemm: Um be good to bounce ideas, I guess, off each other.
Alex Del Re: Yeah. Yeah.
Joseph Boyer: as as we go through and develop starting with the auto loop and whatever managers we get to when we have to-dos that we need to come back and do later or things that we see need to happen. Where should we be throwing those tickets so that they don't get lost and everyone else knows that they exist?
 
 
00:06:31
 
Joseph Boyer: You're mute.
Alex Del Re: I'm sure you can hear me in person, but um yeah, so uh just going on mute to avoid feedback. Um but like the idea is if there's a ticket for like let's say for auto loop that like you know you need to do but it's not necessarily in scope for this sprint or the next few sprints that's where you just create you know create the ticket. Uh I I don't want to create it now.
Joseph Boyer: Mhm.
Alex Del Re: So I'll just show you a another ticket. But just looking at this epic, you would put it under the uh like to-do or um the backlog. But probably not to-do, you do it under backlog. And that's just a way that we can register that the ask or work is documented. And then when we go through sprint planning for you know 26.13 or anything subsequent to that, we'll look at what's in backlog. it wasn't active development and kind of shuffle them
Joseph Boyer: What types of views do we have to see what the backlogged work
 
 
00:07:28
 
Alex Del Re: in.
Joseph Boyer: is for the STV application without I'm hoping we don't have to go into all these child work items and see everything.
Alex Del Re: Oh yeah, definitely not. I mean, so like I have filters set up. I I don't know if you guys have ability to create these on your side. I can double check. Um but like this is where I would say we would create a you know filter for all
Joseph Boyer: Gotcha.
Alex Del Re: issues in the SDV initiative. Then you know you can filter by uh and uh o Jake's mad at me. Why can I click enter? I guess it's oh shift enter what I got to do and then you can do uh what's status I think it's called and
Joseph Boyer: Sure.
Alex Del Re: then you do in and then you do like backlog or I don't know the exact same text off the top of my head but you can kind of get the gist of what I'm trying to say.
 
 
00:08:29
 
Alex Del Re: Yeah. So what I'll do is I'll take an AI to create a filter for um SDV software backlog. Oh, and there's Timothy.
Mike Lemm: This is this is where one of those asks I guess comes in with the ability
Alex Del Re: Cool.
Mike Lemm: to make like sprint boards and whatever because it makes the viewing of all that type of stuff really
Alex Del Re: Before
Mike Lemm: easy. Um I mean fil filters are are good but digging through that JQL is a little little cumbersome. Um so yeah, I think some of that would help. Anyway, I'll I'll turn it over to We got Tim here.
Alex Del Re: we do that, I guess Mike, like you're talking about like something like this, like a a dashboard for kind status. I know like this may not have the exact content you're thinking of,
Mike Lemm: No,
Alex Del Re: but Oh, go ahead.
Mike Lemm: the dashboards are are nice. That's probably another John Lee type thing. Um I mean, we could use it as well.
 
 
00:09:37
 
Mike Lemm: They're pretty.
Alex Del Re: Dashboard.
Mike Lemm: Uh, but on I don't know if you guys are familiar with the sprint board since you're using that sprint v2 custom field. Um, but this the sprint boards just list everything in the backlog. You don't have to go and I mean your filters would basically just be like I want to look at this project and these epics or whatever and it would just list out everything. It's like the alternative to the the conbon board here.
Alex Del Re: I see. So it' be like the summary here and you kind of condense it or maybe the timeline here and you condense it based on a given epic or something like
Mike Lemm: Uh it'd be it'd be closer to the all work tab.
Alex Del Re: that.
Mike Lemm: Um but it's already filtered out by like it it's removed all of the things that are done, which I don't think this one does. You'd have to manually filter that. Uh yeah.
Alex Del Re: Yeah,
Mike Lemm: So anyway,
Alex Del Re: gotcha.
 
 
00:10:31
 
Mike Lemm: there's some different things we can play with.
Alex Del Re: Gotcha. Yeah, I mean this one's what we have for the virtual tool chain stream. It's like I just quickly created it us also not filtering by the virtual tool chain stuff. But um I I hear what you're saying. Uh shouldn't be too bad to create. Just got to create like the overarching filter and we can go from there.
Mike Lemm: Yeah. Okay.
Alex Del Re: But yeah, associated board. Okay, cool, cool, cool, cool, cool. Um, I see Timothy, you've joined. Um, I kind of teed you up for a quick introduction at the start of office hours today, but um, we have some folks from the Kamasu side on the call and, uh, we're just hoping you can give them like a quick introduction, you know. Uh, yeah.
Timothy Kyung: Yeah. Hi. Um, so my name is Timothy. Uh, I just joined the Appenge team uh, here at Applied.
 
 
00:11:25
 
Timothy Kyung: Um, so I'll be working with Alex to support you guys. Um, prior to this I was an application engineer at a company called Math Works for about six years. Um, so you know, hope to get up to speed um, quickly and help you guys out as soon as we can.
Joseph Boyer: Nice to meet you.
Timothy Kyung: I
Alex Del Re: Yeah. So Tim Yeah. So Timothy is going to be helping out a lot with uh kind of the support arm that you know we've been focusing on. So there's kind of two halves to the Kamasu SDV work. there's like the actual application development and then there's like the support and uh documentation buildout. So like we're going to be tag teaming both of those um to kind of make sure you guys have what you need moving forward. Uh yeah, so uh for today um we had some stuff from yesterday that I wanted to follow up on. Um, see, uh, we had like an, uh, Lauren was, not Lauren, sorry, Ashley was mentioning yesterday about for each one of the, let me pull up the doc.
 
 
00:12:38
 
Alex Del Re: each one of the managers that uh we're working on developing for um we should have like a specific meeting set up um to kind of talk about you know IO zone allocation and the success criteria there um identify the person on the applied side to have in those meetings but I'm just curious um from the kamasu side like is it primarily going to be you Joe that are going to be in those meetings or should we think about having other folks on a per app
Joseph Boyer: should should be all four of us.
Alex Del Re: basis.
Joseph Boyer: Um, anything that's links is probably fine with me, but anything that's not links,
Alex Del Re: Okay.
Joseph Boyer: as we get to those, we'll have a a another Kamatsu system engineer involved.
Alex Del Re: Okay. So I think like looking at this list uh Timothy for your context what I'm sharing is kind of like the prioritized development uh for the different managers that Kamasu is looking at. So um in terms of the Kamasu DRRI it'll be the four folks on this call.
 
 
00:13:44
 
Alex Del Re: So that'll be what at New Why is your name not up? There we go. and then at at Jonas. Okay. And then those would be for the links applications which I assume does that also apply to enhanced brake and steering or is
Joseph Boyer: No,
Alex Del Re: that different?
Joseph Boyer: that would be so it's basically going to be us four for all of these and then
Alex Del Re: Okay.
Joseph Boyer: also Jason Shepler and Nick Sturm and Joel Hatterman where they're listed as DRIs.
Alex Del Re: Okay. Okay. So, you guys are just blanket apply to everything and then we'll also include the other folks.
Joseph Boyer: Yeah. Yeah.
Alex Del Re: Okay. Gotcha.
Joseph Boyer: Yep.
Alex Del Re: Gotcha. Gotcha.
Joseph Boyer: Since we'll likely be working on all of us, it'll be good for us all to be a part of these discussions anyway.
Alex Del Re: Okay.
Joseph Boyer: So we can also have um operator displays though would not be I'm guessing that's going to be a separate workflow.
 
 
00:14:40
 
Joseph Boyer: Same with the service screen display
Alex Del Re: Gotcha.
Joseph Boyer: UI.
Alex Del Re: Okay. Okay. So, anything with Anthony is kind of or Tony, he's like his own his own thing.
Joseph Boyer: Yeah,
Alex Del Re: Okay.
Joseph Boyer: we won't be the ones doing that.
Alex Del Re: Um, how sad. I thought I could copy and paste Google names, but I guess not. Let's see. And then let's see. Okay, that that makes sense. So, Joe, I'll probably just peek at your desk at some point today to bother you about uh just finding time on everybody's calendar. Um,
Joseph Boyer: Yes,
Alex Del Re: god,
Joseph Boyer: sir.
Alex Del Re: this is ridiculously annoying when it comes to adding in names. Um, what do you call it? Uh, yes, because like this is a big uh focus by Nick Nick Dars, sorry. um about uh planning for the upcoming release and like what what development is going to look like moving forward.
 
 
00:15:46
 
Alex Del Re: So we want to get these subsystems IO's and zonal allocation set as soon as we can.
Joseph Boyer: Yes sir.
Alex Del Re: Okay, cool. And then um the other thing I wanted to look at was Yeah, I got a question from the like the OTAA and the DIAG team. Um, generally like uh they were asking for how do you at Kamasu think about um sorry just trying to find the exact wording they gave me. think about like manufacturing verification down the line like for your applications. Um like they're discussing Q2 and Q3 planning. Just want to make sure that like when you guys get to more productionized applications, I know this might be a bit ahead of where we are right now. Um uh like are there processes you guys have defined for the verifications of of these apps at end of line
Joseph Boyer: uh for the apps themselves or for like the truck
Alex Del Re: I guess like for you like when the truck is getting built you'll have the controllers on the truck and then you deploy your software to
 
 
00:17:03
 
Joseph Boyer: build.
Alex Del Re: them like um I assume there's some sort of integration level test or system checkout that you guys perform. arm.
Joseph Boyer: Yeah. Yeah. We have a a whole uh what we call a kind of
Alex Del Re: Okay.
Joseph Boyer: a low voltage test where we go through and we validate all of our sensor readings and stuff and then we have um some more functional checks tests um validating the hydraulic systems um the drive system has its own set of tests um part of the initiative that I've
Alex Del Re: Awesome.
Joseph Boyer: started um and that is kind of harping on indirectly. Um, and some of this is the elimination of live work um and automating some of those. So, previously those have all been very manual processes. Um, so we we're with the links project we're in the process of automating some of the hydraulic and high voltage tests. Um, so that's one of the process that's one of the things that I want to understand as kind of a down the line thing of how that fits into how that will fit into our STV application.
 
 
00:18:23
 
Joseph Boyer: Those processes, those automated checkouts as we've been calling them.
Alex Del Re: Mhm. Yeah. So like on at the end of line or whatever you guys call it, that's what we called it at GM,
Joseph Boyer: Yep. Yep.
Alex Del Re: but like at end of line um how can you just like click a macro and it runs these tests for you rather than before which was like a very user intensive process.
Joseph Boyer: Yep.
Alex Del Re: Okay. Yeah, that makes sense. Um and then
Joseph Boyer: And a a note on that is since our things are so big,
Alex Del Re: like
Joseph Boyer: they have to be disassembled before they get shipped out. So all these things have to be run again at the customer site. So, we do it once in the factory to make sure there's no issues there.
Alex Del Re: uh
Joseph Boyer: And then we have to tear it apart, ship it in parts, and then build it back up and run those same tests again at the customer site.
 
 
00:19:11
 
Alex Del Re: Yeah, this is like there's that kind of opens up some more questions on like how uh like the medium in which these tests should be run like should they be embedded into the software platform itself?
Joseph Boyer: Yep. Yep.
Alex Del Re: Should it be some sort of hardware you plug in to kind of execute the tests?
Joseph Boyer: it should be embedded into the software itself is the answer to
Alex Del Re: Um Okay,
Joseph Boyer: that. We want to steer away from external sources if we can.
Alex Del Re: gotcha.
Joseph Boyer: Um, and we've actually scoped out the all the the IO that we've done. We're planning on having all the sensors and readings that we need to perform all those high power tests. So all the things that they plug into and read and stuff uh SDV will natively have access to all the that information.
Alex Del Re: Gotcha. Okay, that makes sense. Um, yeah, I'm going to relay this info to, um, uh, was it Leang and Ginder?
Joseph Boyer: Yeah,
Alex Del Re: They're like kind of talking about what these kind of things are going to look like for y'all moving forward.
 
 
00:20:21
 
Alex Del Re: So, I appreciate the context and clarity there. All
Joseph Boyer: I'm curious if you guys have We don't have an elegant solution for our low voltage
Alex Del Re: right.
Joseph Boyer: testing. It's basically you walk around the truck and you flip switches and unplug things and make sure that you get the correct um response on the user interface um for every sensor and every output and every input on the truck um as like your first initial test just to make sure everything's plugged into the right spot and all the sensors exist. Um be curious to see if you guys had any solutions
Alex Del Re: Mhm.
Joseph Boyer: there with stuff that you've seen or
Alex Del Re: Uh,
Joseph Boyer: not.
Alex Del Re: I don't have any off the top of my head. Um, I mean, the first place I'd look is our docs, but not sure if anything exists there. Uh, I'll talk with um them to see what we have in place right now.
Joseph Boyer: Yeah.
Alex Del Re: Um, I'm guessing I I don't want to guess, but um I'll I'll talk with them and then we can either have another meeting or pull them in to
 
 
00:21:23
 
Joseph Boyer: Sure.
Alex Del Re: office hours to kind of talk about that maybe next week. Okay. Okay. Um and then one other topic. Um see sorry I'm just trying to find it in my notes. Um, now the other thing was I have to work on that hill timing board that we discussed, Joe, that we all discussed, but um, I realized I didn't check it off yet, so I haven't been able to work on it yet. Um, let's see the other thing. Okay. Yeah, that's all I have for right plan for today. I know like we're going to be looking at um the hardware after office hours today in terms of like how to deploy. Um I'll see if we can get a room for that so Timothy you can watch if if you have free time but um any questions from the Kamasu side that we can talk about right now?
Joseph Boyer: Do we have any sort of schedule for ongoing or or to-do discussions that we've discussed in previous office hours?
 
 
00:23:04
 
Joseph Boyer: Just curious where those stand.
Alex Del Re: Yeah, the ones that I'm aware of off the top of my head are the signal gateway. Um, we're still I'm still talking with the team to get the right documentation to show to you guys in terms of an example and kind of how to best structure your signal gateway. Can we do sub signal sub gateways per application stuff like that or uh interfaces per application and stuff like that. Um we have the diagnostics and fault management inject fault injection validation that uh Joe we talked about earlier today. Um don't have a meeting set for that currently but um hoping to have that done next week once I am able to work through the workbench uh updates. Um the other thing that we wanted to talk about was um having a hill discussion. I'm working with uh Alberto, not Alberto, Alberto, Raul on our side to kind of have him join office hours or some other meeting um to discuss like what hill testing will look like. I assume we'll pull in Eric or Tony maybe on those on those discussions.
 
 
00:24:16
 
Alex Del Re: Um probably both.
Joseph Boyer: probably both.
Alex Del Re: And then um what else? And then I had a brief meeting or an an initial meeting with the displays team about how we're going to communicate the um communicate signals to like a user display service interface and um like those are the two that I that we talked about. Uh so that is what I'm still digesting the information from that. So hoping to have that meeting either Friday. Uh, I guess to directly answer your question, I have a bunch of topics in the air. Um, don't have exact meeting time set to discuss them with y'all yet.
Joseph Boyer: Okay.
Alex Del Re: Yeah. Um, I guess across those four that I just mentioned, I'm sure there's others, but um, the priority ones in my mind are signal gateway and diag. Is that correct?
Joseph Boyer: Yes.
Alex Del Re: Okay.
Joseph Boyer: Yes.
Alex Del Re: Yeah, I guess I've regressed to taking handwritten notes and um the flipping back and forth is slowing me down.
 
 
00:25:35
 
Alex Del Re: I know I get looked like Anyway, yeah, I digress. Okay. Um yeah, that'll be once we go over hardware today in person, that'll be my focus to make sure we get those lined up. I know I've been talking about signal gateway for about you know five days or so. So yeah, any other questions from Kamasu side? I guess uh Newan were you able to figure out that I saw you messaged me or DM' me but I didn't get really a chance to take a closer look. Were you able to figure out that issue we were just talking about about the consumer
Nuthan Sabbani: Yeah. Uh I found an example while I was digging into light controller app.
Alex Del Re: Cool,
Nuthan Sabbani: Uh I think it it is fixed now. Yeah.
Alex Del Re: cool,
Nuthan Sabbani: Okay.
Alex Del Re: cool, cool.
Joseph Boyer: Jonas, Mike, have you guys had any chance to start crunching through some auto loop stuff?
Alex Del Re: Um,
Joseph Boyer: I haven't had much so
 
 
00:26:41
 
Jonas Hageman: Yeah, I've started um started that process in the in my own
Joseph Boyer: far.
Jonas Hageman: branch. Um I haven't gotten too far gotten to the like the creating the software components. Um, but yeah, just been playing around with it, trying to work through the docs or the the guide that we made and the requirements that uh we wrote to try to, you know, go through that process of reading the guide and looking at the requirements and turning that into code and seeing where the gaps are.
Alex Del Re: Yeah, I guess Jonas,
Joseph Boyer: Understood.
Alex Del Re: as you work through that, you know, um if any blockers come up, you can grab me. I'm here or, you know, post in the channel.
Jonas Hageman: Thank you sir.
Alex Del Re: So,
Joseph Boyer: Shall we flash some hardware?
Alex Del Re: yeah, let's do it. Um, I think we can adjourn the office hours for now. Uh, Joe, are you thinking about doing this in a room or kind of just at the desk we have back here?
Joseph Boyer: Uh, I think the desk would be fine.
Alex Del Re: Okay.
Joseph Boyer: Um, we want a room.
Alex Del Re: Um,
Joseph Boyer: We can probably find one.
Alex Del Re: no. I think it's fine. I'll uh trying to think what the best way to do this would be for Timothy. I'll like uh talk about like this process with you after the fact. Um maybe
Jonas Hageman: Are are all four of us going to convene at somebody's
Alex Del Re: I'll think so.
Jonas Hageman: desk?
Joseph Boyer: Yeah, just behind he's got it set up behind Jason here.
Alex Del Re: Yeah.
Jonas Hageman: Okay. Okay.
Joseph Boyer: If we want a room, we can always see what rooms are open. Thank you.
 
 
Transcription ended after 00:28:48

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
