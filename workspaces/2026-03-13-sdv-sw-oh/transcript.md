
Mar 13, 2026
Katana <> Applied: SDV SW Office Hours - Transcript
00:00:00
 
Timothy Kyung: Hi Joseph. Sorry. Can you hear me? Uh, I don't know if you're talking, Joseph, but I am unable to hear you. Hey,
Alex Del Re: Hey Timothy,
Timothy Kyung: Alex.
Alex Del Re: we're in the room with Mike and Joe. How's it going?
Timothy Kyung: Never mind then. Or is Joe different than
Alex Del Re: Happy Friday.
Timothy Kyung: Joseph?
Alex Del Re: Joseph is the same as Joe,
Timothy Kyung: Okay, perfect. Never mind.
Alex Del Re: but you have to call him by his full name.
Timothy Kyung: I
Alex Del Re: So yeah, just okay. Uh let me share notes for today.
Timothy Kyung: Just
Alex Del Re: Um yes. So I wanted to use this time today to you know answer any open questions from the Kamasu team and also kind of discuss the plan for next week. um in terms of topics for discussion. Um does that sound good from Mike and Joe's perspective? Yeah. Okay. So, um looking at I showed the wrong tab, my bad.
 
 
00:03:48
 
Alex Del Re: Um sent something else. So, looking at the plan that we talked about last I think it was last week or a week and a half ago, whatever it was. Um we're planning to talk about recommenal injust injection testing on Monday. Um uh go through an example of that and I just want to make or understand um there's been a lot of like conversation uh in terms of like these different topics uh where there still are gaps from the Kamasu side. Um, I've been talking a bunch about autosact development with Newton and he's been kind of working through an example with Shisty and the middleware time middleware team from our side. So I think he's got a good sense of the application development process test case communication test case definition and then I'm providing him some examples for inner zonal communication. So uh I'm kind of leaning on him to proceed or tell me when he's blocked on those topics. So I think for you two like the um things that I assume you want to focus on and kind of what we've been talking about are embedded testing and implementations there which we talked a little bit about yesterday.
 
 
00:05:01
 
Alex Del Re: Um but uh is there like time you guys want with like someone on engineering for that? I mean we kind of had Ashley step in and out but want to hear your thoughts there. I mean, yeah, that's something that'll be something we need to understand. I think it's imperative for like our next couple of sprints. Um, but at some point, yeah, that's going to be knowledge that we need to be familiar with. Okay. I mean, like, is that um outside of like the docs that we shared on embedded unit testing? like um I thought you were talking I thought we were talking about deployed debugging like once the application is deployed onto the palm what tools do we have I'm sorry were we talking about different things uh I was talking about um like implementing a test case uh in your codebase to test the firmware that you're writing essentially unit tests I think we're good and we're going to discuss more still workbench tests on Monday, right?
 
 
00:06:10
 
Alex Del Re: Yeah. Yep. Think we're good there. Okay. Um like GPIO uh input output. I think we covered how to do that with Pyarchch or No, we've seen HSDs and E fuses. We haven't seen any inputs as far as I'm aware. Okay. We can talk about that today. Imagine it's pretty much the same thing, but be good to have confirmation. Yeah, Jonas was asking some questions on HSD's ES yesterday, but um we can talk about what uh what I shared with him in terms from the PI arch side. Okay. And then in zonotal modeling, I think we kind of talked about from Pyarch in terms of like defining the senders and receivers for different zones. Yeah, correct. We still are waiting on a suggestion from applied of how to do our endos communication but everything we've seen so far is CAN message on Ethernet which does not seem like the most elegant solution for our setup.
 
 
00:07:17
 
Alex Del Re: You have a more ideal solution in mind? Ethernet. Ethernet. Just straight Ethernet packets. Those when we started this, everyone thought it was going to be DDS or some for of Ethernet with a just straight Ethernet package that are less rigid. Be a little be a step in the right direction. Um at some point I would like to if it's if the functionality is not already there um with those PDUs that are interzonal PDUs where we're defining both the send and the receive um to have a more automated um PDU build process instead of defining the um the start bit location, the signal length and stuff. The signal length probably could keep both especially like the the building of the packet, right? The the structure doesn't really matter because we're defining both the send and the receive. So I can see scenarios where it gets to be a pain in the ass of us having to define that structure if possibility.
 
 
00:08:36
 
Alex Del Re: So or can that makes sense because we're only defining one side but we're defining both sides. It' be nice to have some flexibility there and not be not have it be so tedious. Sure. Okay. Got it. All right. And then um yeah, diagnostics. Uh like I said, there's a PR that we're trying to merge in to get the Irene implementation into uh your codebase. Um for diagnostics, so that's coming hopefully today. Um then uh and signal validation. We talked about this. still talking with Evan who came into office hours last week I think it was to talk about how we can build out maybe a more custom hand signal validation process for y'all because right now we level or relever very heavily on the autostar um I think it's like schemas 2 and 11 or something like that but yeah whatever they are um we use those oops And then okay so yeah we'll plan to have a discussion on that next week and then yeah yeah okay and then um for fault definition implementation that'll come with the docs and then uh or the the codebase implementation we'll review that together in office hours and zonal event monitoring um what do you call
 
 
00:10:13
 
Alex Del Re: it uh this is so what uh in a given zone like auto lube consent an event and have that pass to other different zones and then have those so auto loop is in frontal um have rear zone monitor any events that are coming from the front zone that are set by uh I guess a runnable in this case. Yeah. Okay. I'm guessing that's just going to be really any DTC. And so if we have DTC's that are set by um like can signal like the E2E if if we have a I guess I'm not super confident that I know how um we would set a uh DTC based off of CAN signal integrity. Is that something that we explicitly have to do in a runnable or is that something that is handled by piearch and the like class? Um I I don't know off the top of my head. I know that if you define um like let's say a can signal in piearch to communicate across zones there is inherent diagnostics we run at that software layer or the diagnostics layer that will monitor um from a CRC perspective those CAN signals um but I don't know what the mechanism is to like set a DTC if that signal is not received or doesn't meet that check I think Um, yeah, I don't know the answer there.
 
 
00:12:12
 
Alex Del Re: Okay. Yeah, I mean like if it's something that you've implemented from the application side, um, I can see that getting pretty hairy. Uh, that's what we do today. So, it's Yeah. Okay. A deal breaker by means, but yeah. I mean, like if from the application side, if you think about it, what could it look like? you have nice to be from the application side because a lot of times we have masks okay on those faults based off those startup shutdown procedure options etc. So, so mass based on the state that you're in. Yeah. For the truck options, what's configured? Obviously, if that um component doesn't exist on whatever truck you're on, then you're gonna ask that. I remember talking about this with Evan. Give me like one second before I throw over. So what is the difference between an HSD and an EU output? Sorry. Okay. Uh before before I answer that, um uh what do you say?
 
 
00:13:49
 
Alex Del Re: What do you say? uh for like the when you when we have an invalid signal received right now um uh if we don't pass through the CRC check we receive what is called a data store invalid uh message uh that would be received to the f the software component uh no sorry that's received by the diagnostic layer for that given CAN signal um but right now once we receive one of those we don't really do anything or or flag any errors we just drop the frame from the diagnostic side. Um the team can explore adding a dem event which is like that level one through four I was talking about the other day in terms of like critical or yeah log or it's like critical scheduled from a shutdown perspective or L2 L3 which are like logged events. Okay. Or it could set a DTC. Okay. Um, so in theory, we could set a dev event that's lowle and then use that, read that within software to then set a DTC based off of masking conditions.
 
 
00:15:00
 
Alex Del Re: Uh, I think so. The masking side, I I less context on how that could be done, but um, yeah, from like the basic functionality, yeah, seems seems about that. Okay. Um, and then sorry the other question was efuse versus Yeah, I was reading your response to Jonas of how HSDs are ef controlled. Mhm. So we have efuses and HSDs in the calls at least for these outputs. Are those hardware different? Are they the same? What's the the what the call to the actual output to the hardware? What is an HSD and what is an efuse physically? Not necessarily the calls and priorities like what's different physically on the board. What is different between them? When would we use HSD? when we when we need EUS output I mean physically the like the HSD is like the high side drive which is what we're trying to do to drive 24 volts to your components in this case um output not a high drive EPU is not I I always assumed the efuse was kind of like the how do you say like the the check or mechanism that ensures we're not going to trip the output of the pin in this case.
 
 
00:16:36
 
Alex Del Re: Um, and the HSD interface is actually what drives the signal or so the message to the pin. Okay. Is that Yeah. So they're in line with each other. Yes. High side drive that goes through an efuse. Are they routed in series or is the EU a logical check on the circuit? from the application perspective like you don't need to think about applying the efuse because from piearch you would define the HSD or the signal to go through the HSD um and then in the underlying implementation of that uh HSD interface it routes through the efuse uh implementation that's what they meant to find it but there is chunks of code in the headlights where it was calling out efuse outputs outputs And then it was calling EPS along with it. That's why this is stemming for me. Okay. So maybe um I'm missing something here. She calls it out in controller SWC. Pi.
 
 
00:17:41
 
Alex Del Re: I'm trying to see what pins they're actually tied to in the connections. Yeah. So we got rear right and rear left stop light and then service brake lamp. Yeah. There's there's PPHSD outputs and then there's PPEs outputs. Uh what's the file you're looking at again? Sorry. System.py is what I'm looking at. Client 105 is example. Client 101 example of a HSD output. Uh, could you share your screen just so Timothy can also see it? I'm looking at the same file in my code editor. I was looking at these two differences. We're calling an HSD output versus an AUS output. Both for just headlight control outputs. Um, and then in PI, the system controller where she's defined the different lights. She has HSD lights and Euse lights, which is I remember commenting on this saying it's because she ran out of HSD pins on the P. Yeah, I guess I don't have good context here to answer.
 
 
00:19:10
 
Alex Del Re: Um yeah, my interpretation was that like if you define an HSD it should handle the efuse logic for you. Yeah, but I guess that's wrong. Um also another big assumption that people uh particularly on the hardware side have been making is that we're going to have software access to like the current draw out of these EUs outputs. Um, that is a a big request that they've just been kind of figured it would be there. So, it's a question that I would like to throw out there. Do we have any visibility from an application level of the current draw out of these? Um, yeah, I think we do. like that's something we're building into sill right now for your testing and who's working on the HSD implementations from the vehicle side from our discussions it was as long as we define or uh yeah because he was explaining HSDs to me and like because I was kind of learning about what they are and he was saying like typically like HSDS is more just like a binary on off like you can get feedback into actually what's running through the system that's something when he explained it to me, he mentioned it as something they're building into the platform.
 
 
00:20:40
 
Alex Del Re: As long as it's a future capability will be available by 2027, whatever our Arizona data is. I just want to make sure that that's on the road map and that's not something that you're like, no, I mean, good good calling it out now. Uh, I'll confirm with him and then if it's not on the road map, we'll get it on there and out before 2027. Yeah. Yeah, that's a good I mean that's some buffer time, but we need to get it to you earlier so you can have like some more time for testing and stuff. I'm reading through some explanations on why system PI has HSD and EUS defined in the same file. Yeah, it's not exactly clear right now. I'll have to get a great better answer for you. Okay. Yeah, I guess like um Joe, you're highlighting this part. Let me just double check. H just lights list and then if you go back to the system.py pie. Um, I think these are Yeah, I got Never mind.
 
 
00:22:40
 
Alex Del Re: I'll get the answer for you. Sorry. Yeah, those are two different outputs for the same thing. Yeah, not for the same. Well, two different uh types of outputs, correct? Yes. both very separated, but like the efuse port is outputting to two two different things. The same kind of port in this sense like the Yeah, I'm picking up what you point out. Like the efuse abstraction port can output either an HSD or an EU. And they're both used as outputs. They're not like used in tandem. Yes. Yeah. This software output has a output and an HSD output. Two different software outputs. One on HSD. Cool. What the difference? Okay. Um All right. And then one thing I forgot to mention for next week is we're going to do like hardware setup. um I don't know what that's said or something like that.
 
 
00:23:43
 
Alex Del Re: You said there was a positive movement on the uh they have tracking numbers but they when I checked this morning they hadn't left be okay. Um, yeah. And then one thing I wanted to show JoeMike Timothy. Oh, no. We looked at this yesterday. Never mind. It was just going to be the app dev schedule, but we looked at it yesterday. Um, this guy. Yeah. Yeah. Yeah. Timothy, have you seen this before?
Timothy Kyung: I have
Alex Del Re: Okay. Our discussion with Tony Hes scare me. Yeah. Um, we need, yeah, we need to figure out uh have a better uh what is it called? Um, we need to have a stronger conversation on like what the hes actually mean from a testing perspective. Yep. What's feasible for this initial prototype? Yeah. Like what controllers can we actually get on there?
 
 
00:25:03
 
Alex Del Re: Yep. just what that testing sequence is, what those testing sequences are going to look like. Are those going to be completely redundant logic checks or are those going to be um something else I pray that it's not completed checks those historically have not moved that um but Timothy for your perspective um this is part of like this architecture and planning discussion we're having for subsequent releases. Um, each one of these kind of RDTs uh are different applications or managers that the Kamasu team is going to develop. Uh, so we're trying to figure out a reasonable timeline uh that they can kind of like execute on for like these different apps um to support the R which is like requirements gathering, D which is the actual development and T is like the software testing and then H is hardware testing.
Timothy Kyung: So like I was going to say like a giant
Alex Del Re: But how can we make sure Oh, go ahead. as a system.
Timothy Kyung: heart.
Alex Del Re: Yeah, kind of like a Gant chart.
 
 
00:26:12
 
Alex Del Re: I mean, the dependencies in here aren't as clearly defined because I wouldn't say these apps kind of depend on each other, but um the whole entire goal laying out this road map is such that we can support uh a prototype vehicle delivery in uh August of 2027. The idea is assuming we can get all this work done before then we'll be able to just like get into the truck, turn the key and nothing will be wrong and we'll be we'll be good. But um we just want to see if we can get ahead of much as much of the integration or other development work that we need here. So um on this list which I'll share with you is you know just kind of list of priorities from the Kamasu side and what apps they want to build and then kind of the key here but this is kind of an evolving list we're planning to discuss with Kamasu leadership next Wednesday. I've been uh making good progress on somewhat solidifying our our meeting on Wednesday to discuss a schematic an initial schematic which would should help cement kind of our controller and zonal allocations.
 
 
00:27:30
 
Alex Del Re: Okay. for these of what the controllers will look like and where will they be living? That's a Kamasa meeting. Yeah. Okay. You think have a better understanding of what our actual I think requirements are. You think it'd be worthwhile to have like someone from the applied hardware side join in? Too early. Okay. Cool. But yeah, uh Timothy, did we look at this yesterday? It's kind of like listing out um it's my first time but the stuff that I've got some of this will change. Yeah. But for each zone um that's running on the vehicle listing out what controllers are going to live there and for each of those controllers like what do they need from like a GPIO perspective where they need to do their job. Um and Joe's compiling this across all the different controllers listed out in that di so all
Timothy Kyung: And this is just a hardware.
 
 
00:28:20
 
Alex Del Re: the controllers needed for those in that diagram.
Timothy Kyung: Sorry.
Alex Del Re: Sorry.
Timothy Kyung: Say repeat what you're saying first.
Alex Del Re: Uh he's repeating this exercise to list out all the controllers that are needed to power or execute those managers we were looking at in the other
Timothy Kyung: Right. And this is just like the hardware requirements,
Alex Del Re: diagram.
Timothy Kyung: but it's not like the design requirements or the system requirements.
Alex Del Re: Uh it's like a bit of both. I'd say in this case it's like the the system requirements to make sure the controllers can can receive what they need but then the that is also in itself like a hardware requirement um more of an IO allocation I think yeah like thinking about like if we look at the the brake controller um what signals does this brake controller need to function so once we lay that out in hardware that'll influence or inform how we're going to do it for software
Timothy Kyung: Okay.
Alex Del Re: at least from a software design perspective and modeling and all that jazz.
 
 
00:29:25
 
Alex Del Re: My attempt to identify the different software component controllers. I see. I see. world different stuff. So, as I'm going through and giving you requirements, I can tell you where these things are going to be coming from because I know the signals that I need to get eventually, but it's not always clear what path that we'll have to take. Hopefully, that'll be much clearer in the next week, week. Got it. Okay. Um, yeah, that sounds good. I think we'll talk more about this next week before we eventually meet with Mike Mike Ricola, sorry. Or I don't know if you guys are meeting planning to meet with him, but I'm supposed to show my stuff to Jeff and uh and him. Okay. Uh any other questions for today? Um depends. Are you running at 11:30? I have another meeting later. I'm curious to see the back end of Docsurus.
 
 
00:30:26
 
Alex Del Re: Is that what you guys are using? Yes. like what that looks like on your doc creation. We're looking at Gitbook right now and before I put in a purchase request for it. I'm just curious what that looks like in comparison, but we don't have to get into a second. Yeah, I mean I'm not the most informed person on docu. I mean, I know we use it to kind of uh read through the different headers, methods, and source files for all our different stuff to generate docs, but um I'll I can find time with our tech writer, Gyra, who like knows it pretty well. So, yeah. Yeah. I don't expect you guys to give me a tour of Yeah. how doourus works, but like but in terms of how we use it, like that's I think that's what you're looking for. It was just like two minutes of like, oh, this is how you would create a doc versus like does it it sounded like it was more coding or markdown versus like Yeah. Yeah. So, but I think it's open source and free. Yeah, it is. It's a very It's very open. It's extensible to how you need it, which is why I think why we chose it. Yeah. Yeah. Uh yeah, I'll I'll find some I'll find time with you for that.
 
 
Transcription ended after 00:31:51

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
