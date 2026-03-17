Mar 16, 2026
Katana <> Applied: SDV SW Office Hours - Transcript
00:00:00
 
Jonas Hageman: and wanted me to admit you. That was weird.
Alex Del Re: Hey
Jonas Hageman: Hello. Hello.
Alex Del Re: everybody.
Timothy Kyung: Hello.
Alex Del Re: All right. Um, I think don't know if Ashley's gonna be able to join today, but we can kind of get started. Um, I guess before we go, before I get into the couple things that I wanted to talk about, um, anything from the Kamasu side that you guys want to raise?
Jonas Hageman: Yes. Um, if nobody else has something, um, I don't know if you saw the message I sent in Slack,
Alex Del Re: Yes.
Jonas Hageman: um, Alex, I know Ashley responded to it, but it was the, uh, packing onto packing an Ethernet frame instead of packing a CAN frame to send over Ethernet and if that's a possibility.
Alex Del Re: Um,
Jonas Hageman: Um because there's a note uh in the docs uh I had sent uh
Alex Del Re: and
Jonas Hageman: in that chat let me see here um it says there are some limitations in the modeling and code generation at the moment that prevent us from directly modeling Ethernet frames.
 
 
00:02:35
 
Jonas Hageman: Instead uh our ETH RX task and ETH TX task directly pack CAN frames into L2 Ethernet packets. there is planned work to provide proper modeling and code generation for ITE 1722 Ethernet frames. So I didn't know um if we were still relying on the packing CAN frames onto the Ethernet bus or just going directly into packing Ethernet frames.
Alex Del Re: I think as far as I know um in terms of sorry this is the first time I'm reading this
Jonas Hageman: That you
Alex Del Re: um I think the the like plan of record is two pack can frames onto the Ethernet. Um, as like as it states in this snip you shared with uh Ashley. Just going to put it in the notes so everyone can see what I'm talking about. Keith
Joseph Boyer: would like to have a discussion on that at some
Alex Del Re: can
Joseph Boyer: point.
Alex Del Re: uh on
Joseph Boyer: The use of ethan, why we're doing it.
Alex Del Re: We talked a little bit about this last like on I think on Friday last week.
 
 
00:03:57
 
Alex Del Re: Um maybe we can just kind of talk about it now. Uh what are like your concerns with using Ecan?
Joseph Boyer: restrictions for the fact that we're packing a CAN frame on an Ethernet bus. I don't know why what like what design choices led us to doing ETH can instead of just Ethernet packets or I mean so
Alex Del Re: originally.
Joseph Boyer: originally all of us I guess all of us the people above us thought that Lee
Alex Del Re: All of us people of color
Joseph Boyer: in in particular thought that we were going to have a more elegant solution um for passing things around. he had DDS on his brain. Um, and yeah, I don't know. Ethan seems like an odd design choice.
Alex Del Re: design.
Joseph Boyer: Um,
Alex Del Re: Especially
Joseph Boyer: especially for our application where we have are going to have a lot of interzonal communications.
Alex Del Re: application
Joseph Boyer: Um, it's mainly from a developer standpoint just ease of maintenance. Um, with a CAN bus, we're limited to what um I can't remember what uh FD is it 64 bytes or something and and we have to explicitly I don't know you guys probably would be able to to change the fact that we have to explicitly do the offset um implementation in there.
 
 
00:05:27
 
Joseph Boyer: So really the only thing is the length from the development side of things.
Alex Del Re: In terms of the length, like are you trying to have like larger messages transferred between zones and
Joseph Boyer: I don't know yet of what our biggest one is going to be.
Alex Del Re: apps.
Joseph Boyer: Um I would imagine payload meter will have a decent amount of data to pass through pass around. Um although I don't know how much of that needs to go on the uh for things to get picked up by the signal gateway even if they're being run on central do they still need to be put out on the Ethernet bus.
Alex Del Re: for things to get picked up by central. Uh right now, yes, they need to be put out on the Ethernet bus to get consumed by the signal gateway.
Joseph Boyer: So payload meter running on central would have to put all the data that it once logged onto the Ethernet ring so that central can pick it up. That's what I'm assuming. Okay.
Alex Del Re: Yeah, that sounds right to
 
 
00:06:35
 
Joseph Boyer: Yeah,
Alex Del Re: me.
Joseph Boyer: there's going to be a a solid amount of data produced by some of these more complex systems. So packing all that into can frames will be cumbersome especially to uh maintain.
Alex Del Re: I mean I think like for packing all those all that data into can frames is like one uh one method of transport over like the Ethernet bus you know like there's this this is the doc that um Jonas was shared the snippet of and like each of these like um frames whether it CAN, LAN, ETH, whatever are all meant to kind of pack into what we call like a PDU or like a protocol data unit. So,
Joseph Boyer: Mhm.
Alex Del Re: we're not strictly limited by um packing a singular CAN frame onto the Ethernet bus. I guess like we can be these are all getting kind of transformed into uh a PDU at each zone like because like running on each zone we have like like kind of like a smaller signal gateway that essentially converts any of this type of information into a PDU.
 
 
00:07:51
 
Joseph Boyer: that CAN frame that you can only pack so many bytes into a CAN frame though.
Alex Del Re: Uh
Joseph Boyer: So that high signal PDU has to fit within the CAN frame. So there's length restrictions on a CAN frame by packing a PDU into a CAN
Alex Del Re: yeah.
Joseph Boyer: frame versus packing it into an Ethernet frame.
Alex Del Re: Sure. But like the what I'm trying to say is um yeah. All right. Yeah. There's nothing else. So if we can only pack a singular CAN frame into one PDU, then there's that limits you guys. Okay. Um do you have any sort of requirements you can give me on like how large you want these signals to be or some sort of like a minimum ceiling or min as a floor in that case?
Joseph Boyer: Um, I don't have a number off the top of my head. No.
Alex Del Re: I think like to help the discussions with the engineering team, it would be good to have some sort of sense of like how large you expect these payload uh signals to get.
 
 
00:08:59
 
Alex Del Re: Um like if the 64-bit limit on CANFD is like really limiting like that's I just want to understand how like blocking it
Joseph Boyer: I can get you a I can get you a struck size of like the pip and hip if you'd
Alex Del Re: is.
Joseph Boyer: like. Though it could be a reasonable start.
Alex Del Re: Yeah, that sounds good to
Joseph Boyer: I can poke Jason for that.
Alex Del Re: me. I guess like you you were mentioning an elegant solution earlier, Joe. Is that like packing into Ethernet? Is that like what you would like?
Joseph Boyer: Um I yeah I don't know um originally we had come in thinking of a pub sub um but it that seems to be from central to offboard or to other things not for the internal ring which is I think where the confusion was. Um, I think Ethernet will be fine if
Alex Del Re: There there is some like work getting done internally that's like slated to get done around the end
Joseph Boyer: we
 
 
00:10:07
 
Alex Del Re: of Q2. too. So like around the June July time frame. Um that is essentially it's not necessarily DDS like you were talking about
Joseph Boyer: Yep.
Alex Del Re: before but it's essentially like some IP yeah directly
Joseph Boyer: IP that would work.
Alex Del Re: sharing um from like payload running on central. It would be able to access um like a some IP topic running on a zone. Um,
Joseph Boyer: Yep.
Alex Del Re: I guess that's kind of like more aligned with this elegant solution you're talking about, right?
Joseph Boyer: Yeah.
Alex Del Re: Yeah.
Joseph Boyer: So, IP was kind of what I had figured after hearing that it wasn't DDS and seeing
Alex Del Re: So,
Joseph Boyer: what you guys supported.
Alex Del Re: yeah. So, I guess the TLDDR is we don't support it yet, but it's going to it's coming on the road map. Um, we have like a simple demo app we could show you probably in April of like it's essentially just like a basic calculator of like central's running this and it it adds on some sensor running in central or off the zone, sorry.
 
 
00:11:08
 
Alex Del Re: Um, but the like the signal flow is essentially central is running some sort of some IP middle uh topic that the zones can subscribe to like that's how like it's like a pub sub thing. Um,
Joseph Boyer: Yep.
Alex Del Re: so do you think that's like like of interest for payload
Joseph Boyer: Wonder.
Alex Del Re: development?
Joseph Boyer: Yeah. Um,
Alex Del Re: Yeah.
Joseph Boyer: I I wonder what the the cost of that is latencywise if if we're going to get into issues with
Alex Del Re: Yeah,
Joseph Boyer: that.
Alex Del Re: I know like on the same zone like some IP will be like really really fast because this is running on shared memory. But yeah, the central to zone latency unclear what that is. I'll talk with Rushi. He's like the guy working on that on the
Joseph Boyer: Yeah, it would just be good to know what the latency is of passing data between zones
Alex Del Re: middleware.
Joseph Boyer: then if it did go to that. I know that's definitely what Lee had in mind.
 
 
00:12:14
 
Joseph Boyer: You're starting with this. I don't know if we need to to do what Lee had in mind, but just throwing that out there. We'll do what's best for the for the actual
Alex Del Re: Um, yeah, of course. That was so weird.
Joseph Boyer: application.
Alex Del Re: I heard you in person, then I heard you. It's like 10, it was like 5 seconds off sync, but um yeah, that makes sense. I think uh like for now uh there's two questions I'll have um raised with the team in terms of like when can we get just packing the regular good old packing of Ethernet messages. Um and then also like what the IP latency is because I think either of those will kind of
Joseph Boyer: Yeah.
Alex Del Re: satisfy your at least from the payload meters perspective um concerns here. Thinking about other apps that could run into like CAN frame issues. Do you have a sense of that now or should we come back to that?
Joseph Boyer: Um, we can come back to that.
 
 
00:13:13
 
Joseph Boyer: I'll look at that offline just kind of what some of the outputs of our link subsystems are. Um,
Alex Del Re: Okay.
Joseph Boyer: I'm trying to think here.
Alex Del Re: Subsystems.
Joseph Boyer: It'll be maybe less on ours,
Alex Del Re: Cool.
Joseph Boyer: but just as a general um like architecture decision for other machines. Um especially if you put in drives. I know drives have some some pretty beefy subsystems, software components that they'll be putting in.
Alex Del Re: like electric drive and stuff.
Joseph Boyer: Yeah. our electric drives controller.
Alex Del Re: Okay.
Joseph Boyer: We're meeting on Wednesday to reassess the scope of that guy.
Alex Del Re: Okay. Um, sorry.
Joseph Boyer: So,
Alex Del Re: Just looking at this good old mirrorboard that I I'm sad that I mentioned during office during standup because every I got I'm getting messages from Lee and John on it. Apparently I shouldn't have said anything. Um,
Joseph Boyer: I'll teach you.
Alex Del Re: but that would be Huh.
Joseph Boyer: method.
 
 
00:14:29
 
Joseph Boyer: That'll teach you
Alex Del Re: Yeah, I guess so. But like that's outside the scope of like the engine interface or is that like is this like something completely separate?
Joseph Boyer: What's the Sorry.
Alex Del Re: Uh the question is you were mentioning like hold on I'm just going to share my screen so we're all looking at the same thing. Um you mentioned uh drives is going to they're going to have like beefy software components like is that wholly separate from the engine interface or is that encapsulated on this
Joseph Boyer: This is the actual drive controller on the truck which is currently not slotted in any of our um development planning. Um we've allocated enough resources to integrate it in but it would be like a a further 2028 goal, a different milestone. Um, and it's undetermined of whether or not it will be an actual milestone for this project or not,
Alex Del Re: I
Joseph Boyer: but we've been doing our best to make sure that our hardware can support it if we do decide to include
Alex Del Re: see.
 
 
00:15:34
 
Joseph Boyer: it.
Alex Del Re: hardware as in the zonal hardware.
Joseph Boyer: The zonal hardware. Yes. And just our
Alex Del Re: Okay, thanks.
Joseph Boyer: processes
Alex Del Re: Yeah, app appreciate the clarification there. Um, okay. Yeah, I think like in terms of like other systems that may cause headache with like the GAN frame limitations, uh, we can come back to that maybe in a couple weeks or so once you've had more discussions. Um, but in terms of what we can
Joseph Boyer: engine interface will definitely be a will definitely be one of those once we get to the actual um full implementation of it because there's a s*** ton of engine data that we pass along um so that we have remote diagnostics of it.
Alex Del Re: That'll be passed along to
Joseph Boyer: Yes.
Alex Del Re: central.
Joseph Boyer: It's just basically regurgitating CAN information.
Alex Del Re: Yep. That's like you guys have a lot of logging built around that, I assume. Okay.
Joseph Boyer: Yep.
Alex Del Re: Okay.
 
 
00:16:37
 
Alex Del Re: Um I think like at least engine and payload are like two at least higher priority apps that I can see that will need this sooner than later.
Joseph Boyer: Yeah.
Alex Del Re: But
Joseph Boyer: And drive drive system will be the same way if we don't either way.
Alex Del Re: yeah.
Joseph Boyer: If it's integrated, they'll have their own BP subsystems. If it's not integrated, then we'll be relaying a bunch of information for them.
Alex Del Re: Uh, and that's that's kind of like dependent on the discussion on Wednesday you said,
Joseph Boyer: Yes.
Alex Del Re: right? Okay. Okay. Got it.
Joseph Boyer: Yep.
Alex Del Re: Got it. Got it. Got it. So, I guess like right now like how do you guys transmit? Oh, wait. Because payload's running on pausing, so it's not as big of a deal.
Joseph Boyer: Yeah,
Alex Del Re: Okay.
Joseph Boyer: a lot of our data is not offboarded.
Alex Del Re: Yeah. Yeah.
 
 
00:17:23
 
Alex Del Re: Yeah.
Joseph Boyer: Um there is a right now we just have a very basic um UDS protocol where we stream data to um uh our what we call our edge controller. So we we stream all of our data via UDS. um just arrays basically in UDS to that and then it um logs that in a database and offloads it.
Alex Del Re: I see.
Joseph Boyer: So the data offloads
Alex Del Re: Okay. Um, any more questions on uh the ETH can ethip discussion. Sorry, I was just thinking back in my head. Okay, cool. And then just want to make sure these docs are shared here so people can access.
Joseph Boyer: for our development right now really doesn't affect
Alex Del Re: Boom.
Joseph Boyer: it, right? Um, it just depends on what frames we put it in and how long how big we can make them. And I don't think any of our initial um, uh, whatchamacallit subsystems should have should be that beefy interal um, engine will get there, but that'll be like a phase 2 version of engine.
 
 
00:18:58
 
Joseph Boyer: I don't think we'll support all the engine logging yet because it's definitely not important for any of our milestones.
Alex Del Re: Got it.
Joseph Boyer: So it should not be limiting.
Alex Del Re: Cut. Okay. Uh, sorry, I was just wring some notes.
Joseph Boyer: on on that I mentioned um last time I don't know if it ever became formal if I can make it formal of a request to have these PDU packings um to be like the the start bit to be automatically calculated um at build time for some of these so we don't have to explicitly define it so it'd be easier to jumble things around Remove signals, insert new ones down the line.
Alex Del Re: Yeah, we talked about that last time. Um, and you mentioned how like it's a bit tedious to kind of like have to manually create a lot of this information. So um what what options do we have to explore for like an automated PDU creation process? So that is something I raised but haven't had heard back yet.
 
 
00:20:28
 
Joseph Boyer: Okay.
Alex Del Re: So once like
Joseph Boyer: I just wanted to make sure that it made a formal request.
Alex Del Re: Yep. Yeah. I don't know if it's like going to be a feature request or something.
Joseph Boyer: Perfect.
Alex Del Re: We just like we certainly support and we just have to like figure out a way to get onto your cluster. But um yeah, I'll let you know
Joseph Boyer: Sounds good. Thank you.
Alex Del Re: there. All right. So, these next two topics that I have here are kind of related um I guess to Jonas and who else is on this call? Yeah, mainly to Jonas and Newton and Timothy. Like we were talking about how Kamasu currently has some internal docs that they uh are creating alongside the home that applied docs to kind of cover like this really uh granular step by step of how to do their development on vehicle OS. And we were kind of just like thinking there should be some way of you know um commonizing that documentation work so we can both show grandma and other like early users how to develop on vehicle OS and have like a sort of easy way for um applied engineering to kind of review and vet that documentation.
 
 
00:21:53
 
Alex Del Re: Um, the reason I bring it up now is because over the weekend um, we added in this uh, new what I would call like co-pilot feature onto um, your your accounts. So essentially like what this looks like is you can ask it questions about the documentation and this is doc any sort of these categories that you see here. So anything from vehicle OS infotainment, the SDK or developer tooling, you can ask this co-pilot a question saying like um what does or what is an I write in the context of PIARCH? And it will what this does is essentially like does like a rag across all of our documentation that we have right now and attempts to find you like a good answer in terms of what is an IED in the context of Pyarchch. Um, and you can see or you can kind of like ask simpler or more complex questions as you guys see fit. Um, does this kind of like make sense to you guys?
Joseph Boyer: Yeah, that's cool.
Alex Del Re: Yep.
 
 
00:23:02
 
Jonas Hageman: Yeah.
Alex Del Re: Yeah. So, um, it kind it'll give you an explanation. Uh what I will say is that uh you guys are very much aware that like we're building out our documentation here and um it can only answer on what is currently in the docs. So like if something doesn't exist um it may give you uh it'll it has this sort of like what I would call like a confidence level ascribed to each one of its answers based on the quantity of documentation that can support its uh prompt. So, if there's not enough documentation, it'll give you a prompt something along the lines of like, I don't have context to answer that question. And then, um, if you have any any sort of follow-ups, you can like continue the conversation here. Um, thinking about, you know, uh, tracking all of these, you know, like you can have multiple conversations and talk across them. And if um you don't if you don't get the answer you want from this conversation, you can say like escalate to um applied and it'll ping me directly or ping someone else on the vehicle team to um talk with us essentially.
 
 
00:24:07
 
Alex Del Re: So then I can more directly answer your question. This is u meant to be kind of done alongside the um sorry the um the the shared channel that we have. Uh, so yeah, if there's no qu any other questions around this, I guess Andrew is currently set as my lead. I wonder what it said. I wonder what it says for like the Kamasu guys here. But um, if you guys have any other questions on this, I encourage you guys to explore and see if your questions can get answered.
Jonas Hageman: Cool.
Mike Lemm: question on your your docs.
Jonas Hageman: Thanks,
Mike Lemm: I guess in general um is are your markdown files uh included with your codebase? Are they all separate or is it some combination of the
Alex Del Re: So our markdown files are included as part of our codebase.
Mike Lemm: two?
Alex Del Re: So we have like a whole entire vehicle OSD docs directory that contains all of that information.
Mike Lemm: Okay. So you're it would be included in the repo, but the markdown for a specific piece of the code or whatever would not be necessarily right next to the piearch file or the C file.
 
 
00:25:24
 
Mike Lemm: They're all kind of just in the docs folder.
Alex Del Re: Yeah, exactly. So, it's all in the docs folder.
Mike Lemm: Okay.
Alex Del Re: Um there some documents like you've seen um have like code references and essentially we have like a special like um I don't know the underlying system. I'll just say it's some extension of docuurs or some extension of basil that essentially monitors given methods or given um classes with like it's like at docs essentially and so you put at docs and you put a document file number or some sort of UU ID and it'll have that portion of the MDX file reference that part of the codebase. Does that make sense?
Mike Lemm: Yeah, I think so. Might have to see it, but I guess I get the idea.
Alex Del Re: Yeah. Um, so that's how you can kind of connect code and that an ever evolving code let's say for um like SDK reference is a bad example but like ever evolving code let's say for like the autosart development like let's say if this this uh command changes over time for whatever reason you can just have that automatically update as you update your codebase.
 
 
00:26:35
 
Alex Del Re: Um, and Mike, I totally forgot why I brought up the co-pilot. Uh, if you guys like, uh, what do you call it? Bring in your documents onto home.applied in this, uh, well, this is like imagine this was like Kamatsu section. The those documents can also be ragged or put into the knowledge base for that uh, copilot I was just talking about. So, in addition to searching our docs, like this could theoretically also search yours as well. if you guys wanted to do
Mike Lemm: Does that I'm not saying I'm uh for or against this one or the other,
Alex Del Re: that.
Mike Lemm: but does that require us to use docysurus?
Alex Del Re: Um, no, it just requires you guys to have your documentation put on vehicle escatana.
Mike Lemm: Okay. Yeah, I' I've been playing with it. There's some overhead with Docsaurus. I guess I I want to see what the rest of the group thinks about it. Um, it seems okay. There's a little bit of little bit of work to it, but it's not terrible.
Alex Del Re: Yeah, I think like it doesn't matter how the documents get produced, but um or how they're managed, but if they're stored in the codebase, we could refer to
Mike Lemm: Seems cool.
Alex Del Re: All right. Um, any other questions for today? All right.
 
 
Transcription ended after 00:28:51

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
