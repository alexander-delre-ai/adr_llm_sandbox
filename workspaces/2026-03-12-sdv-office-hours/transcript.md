Mar 12, 2026
Katana <> Applied: SDV SW Office Hours - Transcript
00:00:00
 
Alex Del Re: Hey, Jonas. Hey, Mike. I'm in the room right outside the pod.
Jonas Hageman: Hello.
Alex Del Re: If you guys want to join me, I think it's called Oh, there you are. Yeah.
Jonas Hageman: I'll pop in there.
Alex Del Re: Trying to find the right line to draw between dropping things in the Slack channels versus the the office hours notes page. Uh, I'd say defer to the Slack channel because I I watch that more regularly. Like I don't really get like a specific notification for um Oh, when the docs get updated. Yeah. Just kind of like that distinction between like lining things up for later today versus like this is a big problem. It could be anybody in the company that wants how to fix it. I like I wouldn't say um what do you call it? The Slack channel should be only for stuff that the whole company should see. It's just like anything that's related to your work.
 
 
00:01:30
 
Alex Del Re: Like it doesn't have to it can be big, small, kind of just like a random question. Like uh posting in the Slack channel like there's no concern about noise in this in this sense, you know, like don't you can just say I mean don't actually do this, but like if you wanted to you could just be like, "Hey, good morning everybody." And like that could be a post in Slack like don't actually but I think you get the point I'm trying to make. Yeah. Yeah. Um so what I'll do is I can um what I can do is I will I lost my train of thought. I will I can create a workflow in Slack that'll just like automatically send out a a call for topics essentially. Um and then that way you can either listen there or you can just put them in the channel. Like it it doesn't matter either way. Yes. Okay. Yeah.
 
 
00:02:19
 
Alex Del Re: So, I'm assuming you got some stuff that you you teed up for today. There was one lingering from before that I still want a better answer on and then something just came up like 10 minutes ago that seems like could be a big deal. You guys have an answer though. Yeah. One sec. Let me see if I can turn off these pings because I am a speaker man today. Here we go. Um, sorry. Just trying to pull up the notes. All right. Can you guys see the docs that I'm sharing? Yeah, one day I'll be able to connect to this TV. I don't know when it'll be, but one day. You need a bigger computer and you can I tried with a dongle and it still didn't work. Um, okay. So, still testing is passing production code incomplete. See example. Yeah, I have example.
 
 
00:03:40
 
Alex Del Re: It's local. Uh local as in like on workbench. No, I haven't even pushed it. I just like I just found it. Um can you share your screen? Yeah. So, I'm just not here now. I mean, the door's not locked. Yeah. It is coming through. Okay, there we go. I don't like this. I like the red border in Teams. Yeah, usually your only your only indication is that little like meet Google at the bottom saying it's sharing your screen. Okay. Um, so in the system.py for PIARCH here, we're defining our connections and let's see here. So we do I I'm still not familiar with all the EU stuff, but we got controller to manager and manager to controller. I'm wondering if we're missing a section here on controller to and from IO that maybe we should break things out so it's a little clear where things are coming and going.
 
 
00:05:05
 
Alex Del Re: Um anyway, what I ran into was where cach is stubbing things out or in my case I've replaced that with some sill mocking. Same thing. Um we've mocked out uh these internal reads and writes or the RTE reads and writes the mocking sill testing is passing because the mock that we're generating are all there but the production code will actually fail because the the functions are missing. So like the ones I ran into here are these the headlight controller. These are like the indicator LEDs. They're just empty functions. So like you wouldn't even know that these are broken until you flash it on hardware and try it. Like the high arch side of this is missing to show those connections so the functions never get populated. Just wondering like do we have a way to find that or am I missing something? So okay so you in the pie arch you defined like kind of the connections in terms of uh what's getting sent from a manager to controller and you're saying downstream um like the actual cubs that get automatically generated um don't have any details in them.
 
 
00:06:23
 
Alex Del Re: So when you actually run the test you would expect a failure but the cach test that you run on the um uh on the codebase actually passes that that's the problem. Yeah. So like in the in the mocked out version here, so like yeah, my my internal writes and reads are populated moving data, but in the production side, they're empty and like you would never know this until you compile it and flash it. Yeah. I mean, because it's runtime C is something you don't actually generate yourself. Yeah. Yeah. Um so like I just I think I was working off of a master from a week ago or whatever. So like I just picked this up wherever Ashley left it and then came across this. So like I think something's missing on the pie arch side. Okay, cool. We can add that. When we get into our system and we've gotund and something signals going on, how you going to know that you've lost it and it's missing?
 
 
00:07:17
 
Alex Del Re: And so you you flash it and you run through all these tests and they like, well, I can never get the headlights to turn on and you got to trace it all the way back to figure out where is it only specific for this? Like is there a pattern at all? Um, so like in this case, which ones don't get mapped? Yeah, this I I just came across this. So like the ones I'm seeing here are like the little LED indicators I think that are on the keypad. So like maybe she didn't have the keypad to work with yet. So she hadn't got that far. Um, so the big concern here I have is like, hey, testing is working, everything's great, let's get a release going. and you go and flash it and like three days later you come across you're like why doesn't this work interest okay no worries um yeah so as far as I know like my best guess is like this reference architecture that we have for you guys is missing some part of the pyarchch model that would populate the actual stubs that go into runtime um I would have confirm this but
 
 
00:08:28
 
Ashli Forbes: Right. What's What's the
Alex Del Re: my uh the
Ashli Forbes: question?
Alex Del Re: question oh I'll wait till he's muted. Uh but the question is uh what do you call it? Mike um was doing some experimentation on workbench code server saying you know he on
Ashli Forbes: Um,
Alex Del Re: the left side of the screen you can see his system pi file where he kind of connected his managers to controllers um and when he did the cach build that all passed and was green but he went to go inspect the actual generated runtime file uh and all these internal ites that you see listed here are empty right or not all some of them are empty because what I'm assuming there's some sort of definition that we're missing here. Um, does that make sense to you, Ashley?
Ashli Forbes: let me look at the exact uh things you're looking at. It looks like the LED state,
Alex Del Re: Yeah. So, and I was saying the concern here is not that we're missing something in Pyarch.
 
 
00:09:31
 
Ashli Forbes: right?
Alex Del Re: The concern is how are we going to know that it's missing before we try to compile and flash on hardware and then find out that it's not working because the tests pass and you got but you'd have to dig into
Ashli Forbes: Yeah.
Alex Del Re: like runtime code to find that it's not
Ashli Forbes: Yeah. So, I mean,
Alex Del Re: there.
Ashli Forbes: I'd have to look at the tests that you're talking about, but at least I can't uh VS Code giving me trouble here. I'm looking for like a high beam LED like parameter. that you're looking at. Um, but I'm guessing this is the one that's connected to the actual CAN portion or like J1939 in this case. Um, and if it's not hooked up to the CAN stuff, which because I'm debugging that today, then like the runtime's not going to connect. But unless right your unit test and this is just like me speaking off the top of my head and I could be wrong but your unit test is like mocking the idea that you do get these uh connections right like the unit test is mocking that you will get something.
 
 
00:10:52
 
Alex Del Re: Yeah. So the unit test replaces it are replaced and the unit test passed and that's
Ashli Forbes: Yeah.
Alex Del Re: all great.
Ashli Forbes: Yeah.
Alex Del Re: The problem is is now you go to compile it and flash it and it actually doesn't work because these functions are easy
Ashli Forbes: Yeah.
Alex Del Re: like that.
Ashli Forbes: So, how I would expect this to be covered is in some form of uh CI there be some sort of sill that like mocks like truly like mocks the input on like a GPIO can or whatever level um like a CAN injection let's say like on a mock bus and then it runs those tests and expects like a GPI output or expects like a different ports and points in the um
Alex Del Re: So you're saying instead of you're talking like a 100 level. So instead of mocking the controller, you'd mock the whole headlight system in
Ashli Forbes: Yeah. Yeah. That's where I wouldn't personally um in my experience I wouldn't expect this level of thing to
 
 
00:11:46
 
Alex Del Re: Okay.
Ashli Forbes: be tested uh found in a unit test because unit tests are like you stub you like you pretend the inputs and outputs are there and how at least from my understanding cach works is that it sort of takes a hold of that like internal IE uh and pretends that it's hooked up to like the cach thing. So the fact that the IRA is not connected um CB will like never know nor care. I can double check that but I think that's how it works and then yeah so I
Alex Del Re: Yeah, that makes sense.
Ashli Forbes: guess like the the long- winded bit bit of a tangent but I think the answer to your question is like how will we find out before we get to hardware uh when the sill or some sort of CI or CD uh infrastructure is in place when we can like a line on what we want to be testing to catch like these sorts of edge cases that it'll be tested checked there before it goes to deployment before it goes to testing hardware test.
 
 
00:12:52
 
Ashli Forbes: But I think there's a real world where you're developing something, you forget to hook it up. I mean, it happens to me all the time. Go to flash, it doesn't work. You look through your code, you go, "Oh, oh crap, I forgot this. Put this in there." But before it gets to um master, that would be the
Alex Del Re: Okay,
Ashli Forbes: case.
Alex Del Re: in this instance there are still test should be catching bad um I rights and I read the definition like where does that what levels at because the the level of sil testing or whatever cop testing that we have right now is replacing those functions Correct. Well, hopefully Monday we're going to start going through how to use workbench and the what's behind workbench to write automated or integration tests which then would validate these reads and writes. It would use the runtime C file. Exactly. And that's where and workbench I guess is emulating that hardware. Exactly. Yeah.
 
 
00:13:52
 
Alex Del Re: So it's emulating it's virtualizing those interfaces such that you can kind of mock those signals. So what Ashley was saying in terms of like mocking the actual CAN signal rather than stubbing out the I or not stubbing is the wrong term like replacing that I write in the actual unit test definition will actually be sending the real signal for it to receive. So we can we can unit test things like we're doing this thing will sit here broken. Yep. And then you get to the higher level and yeah there still part of our CI/CD pipeline. Exactly. Yeah. So like uh don't we can iron out what what the workflow will look like for like how you will make code changes and then deploy and then flash and all that. Um I would assume before you'd make any sort of hardware flashing actually I'm gonna rewind there. I don't know the proper development here but uh we can work that out. But yeah that's the idea with still okay.
 
 
00:14:41
 
Alex Del Re: Yeah if the workbench or whatever we have a way to get to that testing without hardware that' be good because yeah this one just seemed like like how are you going to find that? Yeah, so many signals there go into detail on Monday about how we use work, right? Those test cases. Yeah. Yeah. Just capturing some notes. All right. Okay. Next question. What does this do? And what is this? Yeah, these guys. Um, which one was it? Uh, I think you said headlight manager_ teston only. Is that what you're talking about? Yeah, these test only these guys like so there was this one, there was a this mock kernel interface. Like how are you supposed to know which ones of these you need? Like because I can go in here and comment this thing out and then rebuild it and it runs just fine.
 
 
00:15:57
 
Alex Del Re: Like there's no complaints. So how how am I supposed to know that was needed? Was it autogenerated and just stuck in there? Let me look. Not sure off the top of my head.
Ashli Forbes: The test. Oh, this test only.
Alex Del Re: Yeah. So here I just kind rerun it and everything passed.
Ashli Forbes: Interesting.
Alex Del Re: Yeah. So that it's there and I just ran that
Ashli Forbes: Let me ask let me ask the testing guy because that's in the I follow the same documentation you guys do.
Alex Del Re: target.
Ashli Forbes: So that's in the documentation in the like how to write unit tests. I thought it was a part of a mocking. Um,
Alex Del Re: Yeah,
Ashli Forbes: also, sorry, I'm having a hard time hearing you guys in the room. If you could maybe bring the computer closer to them,
Alex Del Re: I was Yeah,
Ashli Forbes: Alec.
Alex Del Re: I was muttering.
Ashli Forbes: Oh,
 
 
00:16:55
 
Alex Del Re: Um I guess the short update on that is I've got
Ashli Forbes: sorry.
Alex Del Re: the in my mind this is sill but I guess there's a bigger silt. Yeah. Yeah. Um, I've got it pulling from the contract the contract mock file autogenerating all the subs. Um, and then we've got SE in here for units unit testing with COH and then S S testing whatever in here. Um, so you can run the system through time like check a blinker on and off edges
Ashli Forbes: I
Alex Del Re: that as I was going through that the dependencies like
Ashli Forbes: mean
Alex Del Re: where the heck are these things coming from? What do I need? Why is there this mock kernel? I don't know what that does. That kind of stuff.
Ashli Forbes: Okay. Um,
Alex Del Re: So,
Ashli Forbes: can I Okay. Not kernel interface. I think that might have been left over from me trying to experiment with something.
 
 
00:17:49
 
Ashli Forbes: Um, but I can I can go back and double check. Can I ask why you were including the headlight controller itself? I don't think that's typical. Like when you remove that, does that anything break?
Alex Del Re: this guy. Yeah, it's probably going to break. Uh, I mean,
Ashli Forbes: Yeah.
Alex Del Re: you got to call the the function to it.
Ashli Forbes: Yeah. But that should be taken from the contest only. I think that's the idea. What fails? Undefined reference. Can you open up that file head like controller software sill test sorry testc you can open up that file the one that you're
Alex Del Re: See this guy?
Ashli Forbes: writing? Yeah to the top please and thank you. Uh, so you've commented out the include the head like see the thing that says no lint up there.
Alex Del Re: Which one? This guy.
Ashli Forbes: Yeah. So I don't actually think you need the um the RTE like
 
 
00:18:59
 
Alex Del Re: Yeah.
Ashli Forbes: that. Yeah. So uncomment that guy and then that area you have the No,
Alex Del Re: Gosh,
Ashli Forbes: the top the top one that says no link.
Alex Del Re: the mouse
Ashli Forbes: Yeah.
Alex Del Re: lag.
Ashli Forbes: Um, can you try rebuilding it?
Alex Del Re: What is going on here? Now it's okay. So, it's come from one place to the other.
Ashli Forbes: Yeah, I think that's what you've that's what's happened
Alex Del Re: Okay. Instead of including it on the build,
Ashli Forbes: there.
Alex Del Re: you just that I'm not quite following. Like you can include things here, but then you don't have to include in the file, and that just seems odd. And then
Ashli Forbes: Um I think yeah I think maybe the kernel interface is like left in there by
Alex Del Re: a
Ashli Forbes: mistake. Um but generally like with how basil works for these dependencies is if it's not if the path is not obvious or if there's like a bit of like routing it has to do um you have to include it in dependencies but then you also have to include it.
 
 
00:20:12
 
Ashli Forbes: It's sort of like include it in the file. Sorry. So back up. Let me explain that possibly hopefully a bit clearer. Uh how basil works is with these libraries or tests or uh binaries or whatever we have here. You have to tell Basil where to look to find these dependencies and then you also have to actually include them in the file itself. um in order to reduce a lot of like redundancy or to make it a bit easier to follow basil and applied depends on which like target you're looking at and when I say target I mean like the firmware_cc test will automatically package in a lot of stuff so maybe like your your standard libraries come automatically like underlying in the test um or your autogener generated stuff or stuff like that. Uh and then anything additional has to be included in the dependencies there. Um does that make a bit of
Alex Del Re: Yeah,
Ashli Forbes: sense?
Alex Del Re: I think so. We'll learn over time, I guess.
 
 
00:21:26
 
Ashli Forbes: Yeah,
Alex Del Re: Mhm.
Ashli Forbes: Basil was a bit of a learning curve for me too.
Alex Del Re: And I guess Mike to your question on like what's the test only used for I found it something mentioned in our docs. uh just saying you know for every firmware CC library the target that you define in your tests uh the test only target essentially is just like a copy that moves the source file headers into um instead of the sorry it moves the source files under the headers instead of the sources and this allows you to kind of direct tests of those methods for the firmware test. So this is just another way to kind of uh recreate the target for uh unit testing and yeah. Okay, makes sense. No, not clear. It's kind of like um uh yeah, so just like put it on everyone and be done with it. It's it's specific it's specific to like run your unit test on like a Linux system. So like if you think about um trying to directly ac access uh how do I put this u I guess for now let's think of it I I'll get a better explanation for you but for now let's just think of it as like a copy that we use for like unit testing
 
 
00:22:42
 
Alex Del Re: um uh software components. Okay. Yeah. I'll put that as an action item to get better uh clarity on why test only is moving the source files under the headers instead of the sources. Um, yeah, I'm just trying to get an idea of like we go to create a new target like what all do I need to put in it and you know what are they doing just so I know I have an idea of what I'm going to be missing or needing or whatever. Yeah, I think generally like for what you need to put into a new target for like embedded testing like I would say refer to you know the docs in this case like u there's a whole page that we're looking at here about embedded unit testing and uh it should have adequate detail to kind of get you started and get you dangerous I'll call it um and if there's something that's not clear this is where you know I'll work with the documentation folks to like get the get it better you know if there's something that's very unclear we can easily update the doc in this case.
 
 
00:23:38
 
Alex Del Re: Yeah. U but this should have everything you need in terms of the definitions kind of examples for you to follow for implementation and then uh what Oh, I'm sharing right or Mike. Wow. I was just sharing this and then I guess you guys weren't looking. But this is Yeah. Yeah. My bad. My bad. I thought I was sharing. I apologize. Get out of here, Mike. So, um get out of here. Yeah. This is what I was just talking about in terms of like what we have in the docs and then this page that I've just been uh going on on about for the last two minutes. Zooming from the call. It's fancy. Dare you. Um am I in the right spot here for any unit test? Uh if you do control K and search for embedded unit testing K. Yeah, it's like a universal search.
 
 
00:24:27
 
Alex Del Re: Control K and uh search you can search for whatever. Uh which one? What am I searching? So, embedded unit testing and then it'll be that first one. Yeah. Yeah. I feel like a lot of like what you guys are most interested in is going to live in this onboard SDK area of the docs. Um but yeah, this this is what I was just explaining. Um this would have everything you need to get started. If something's missing, we'll update. If um something's not clear, we can also enhance. Yeah. Yeah. Okay. Uh moving through. We've some time left. Um, still unsure on what this does. Is are you still talking about the test only? Yeah. Okay. And then we we also just talked about the mock kernel interface. Okay. Um, cool.
 
 
00:25:16
 
Alex Del Re: Uh, questions from Jonas or your name's not Mike, your name's Joe. Yeah. Um, do we have a like most updated list from where uh what systems are on what zonal? So, I know there's the mural board. I'm working on it. Okay. So, I was wondering for this. Yep. I am aggregating um IO into team controllers and then from there we'll have to make decisions on based off of what controllers are where the managers will live. That screenshot was my Joe do you mind sharing that doc that you're working on just so the team can see the same doc that we had the Excel sheet putting Yep. I've been working out of the duck that you threw in the the copy of it or uh you're talking about You want to wait until it's done. You're talking about this one. Look at it. Um no, you're talking about this one. Yeah, that one.
 
 
00:26:25
 
Alex Del Re: Okay. So, controller SWC. Okay. And I don't know if this is Okay. Yeah. Yeah. Yeah. But, uh I assume you've seen this already, Jonas. Okay. Well, it's I'm sharing it right now. Uh uh this is what um Joe is working on in terms of getting you know for the chassis brake controller for so on and so forth trying to define what are the ins and outs um and then potentially where it's going to live but that still isn't determined that still isn't defined where from a list that is not our schematic so it has differences um I will be changing this uh in the next couple weeks we have a review on Wednesday about schematics of what things will be wired to what. I need to have more of a concrete idea of what sensors will be wired to what zonals and then I can this. This was based off of I think it was actually Nick Ster's guess of where things will go.
 
 
00:27:24
 
Alex Del Re: So, okay, it is not the final, but it should for the most part be. Could the colors mean anything? Um, these are controllers. So that that'll be the hoist controller and that'll be the sensors that go into it. And then the blue are the zonals. Okay. Starts a new zonal your rear. And then the yellow is stuff that I haven't figured out where it's going to what controller to live in controller or what. Okay. Okay. Yeah. I'm assuming this is kind of like halting your modeling in this case if you don't know exactly what it's going to be. Yeah. Because I I also had a question about um the auto. Yeah, the auto auto loop will definitely be in front zone. It'll have a front auto loop zone controller or autoloop controller that'll also live on front zone and then it'll have a rear auto loop controller that will live in the rear zone that just has one sensor.
 
 
00:28:18
 
Alex Del Re: That's what I'm wondering about. Are we going to end up with a bunch of little ones like this? Maybe uh if we should have like a general IO thing that sends out only things that others need. That's kind of what this unknown what these unknown sections are. The things that don't really fit into a thing with other sensors. Um, some of them all have better ideas than others, but I think for that one I'm gonna leave in its own zone or in its own controller. If for some odd reason we add more sensors or a different way to control it, then it's isolated. At least it would just be a small software component, right? I don't think there's any harm in that other than just increasing the number of software components we have. just I don't know open to discussion that's one of the things that I wrestled with a little bit of yes we aggregate as much as we can as it makes sense but is there a point where we should not have a controller for every input type thing I mean yeah I guess like thinking about auto loops it's going to be communicating very frequently with like other zones what's the best way to handle taking in that data Is it the question is no?
 
 
00:29:45
 
Alex Del Re: Rather than creating separated the front zone. So that has a controller that aggregates all those together. It's one nice little controller. Yep. But then there's one sensor way in the back of the truck that's going to be connected to the rear zone. So right now I have it coming in as into its own software component called rear autozone or autoloop controller. And all that controller is doing is reading in that one signal and then sending out and sending it out on the bus. That's that's all it's doing. Um, the question is, should we have kind of a rear IO misfits controller that handles in multiple of those sensors so we don't have a software component that's just reading one sensor or should we keep it separated by function? Mhm. Yeah. I I'll have to talk with the team to see what we did for um another other internal work in this case, but I think like the latter makes more sense to me of like rather than function.
 
 
00:30:53
 
Alex Del Re: Yeah. Um but yeah, I'll talk to see what we've done for other customer work and see what makes the most sense here. It just seems like a lot more maintenance to have to like create a separate component in this case uh for auto loop, right? Yeah. Oh, so you're saying group them. Yeah, I was in the ladder case. Okay. But so like you had rear tail lights and then the auto loop sensor and like some brake temperature sensor like you just group those all into one file, one controller.
Ashli Forbes: Um, yeah, we'll have to take a
Alex Del Re: Yeah. Yeah. The idea there's no it's just a pass.
Ashli Forbes: look.
Alex Del Re: I'm just wondering like is are we going to end up with like every every zone ends up with like this controller that's got this random bunch of jump. Where is that? Oh, it's in the random file that's got 17 subst. That's why I figured we'd still group it by maybe it's better to the function.
 
 
00:31:46
 
Ashli Forbes: Yeah.
Alex Del Re: I was just thinking like at at the pyarch level you're just modeling where it's coming from. So it's not explicit. It doesn't need necessarily need to live in a dedicated component on a different
Ashli Forbes: And this is this is sorry to interrupt but this is um for uh like IO stuff right because we have like the gateway for things that come
Alex Del Re: Correct. This is
Ashli Forbes: in PDUs but not IO stuff and you're asking basically and correct me if I'm misunderstanding but you're asking for basically like what to do if you want a gateway like IO readings ADCs or to other stuff. Do you have Yeah, you're asking or the ask is do we have to
Alex Del Re: Yeah.
Ashli Forbes: make controllers for this every single one or can we just have like a Yeah. What's the recommendation there I guess is the ask, right?
Alex Del Re: Yep.
Ashli Forbes: Am I understanding correctly?
Alex Del Re: Yes.
Ashli Forbes: Okay. Sorry, I didn't mean to.
Alex Del Re: And aggregated sensors.
 
 
00:32:47
 
Alex Del Re: This is all in the rear zone here of okay, these are the controllers for the most part. Sense, but then there's these like four sensors who don't really fit into the other ones and won't be used by or these will just be passed straight on the bus to another zone.
Ashli Forbes: Let me Yeah,
Alex Del Re: Um,
Ashli Forbes: let me see what we did other in other cases and let me see if we can spin something up that would make more sense than a whole bunch of components because I also don't like that and think that's not great because like Uh just so you're understanding my thinking. Um having them separate would be ideal like separate software components because like what if things change around and the whole idea is you want your things to be modular so you can like move them around. But also having all these separate software components just spells nastiness to me too. So I'm wondering if a third option which we should be able to bring
Alex Del Re: Yeah.
Ashli Forbes: something or when I say when I say we should I mean like I'm hoping so.
 
 
00:33:48
 
Ashli Forbes: I have no see what other people have
Alex Del Re: Yeah.
Ashli Forbes: done.
Alex Del Re: Yeah. I agree with you, Ashley. I think like we should look at what options Pyarch will give us in this case and what would make the most sense for your development. Okay. Background noise. So, um, wasn't exactly uh didn't exactly hear what you said, but I think I I picked up what you were putting down.
Ashli Forbes: Oh yeah, sorry.
Alex Del Re: Uh, Yeah. Um Oh, yeah. Yeah. Every zone to me has things on it. The cab is a little less. These I just need to do more. I can I'll have a I'll do better with the cab, but especially the rear and the front will definitely have just a couple sensors that are just going to get relayed to another thing and don't really have a good controller. Any other sensors that it doesn't fit in another group.
 
 
00:34:46
 
Alex Del Re: Yeah, I guess general question here on the zones on the way you split this out. Do you have them split into like roughly equal or like distributed compute requirements or like is the left is the aug zone like just hammered and the rear zone's got nothing? Um not yet. Uh right now it's just based off of where the sensors where the majority of the sensors will go where it makes sense for that compute. Um especially for safety critical things. I know there's more Yeah. As close as close as you can because you take like oh the the fuel system or something like just throw it in the rear and relay all the data back. Uhu. Yeah. Yeah. The the nice thing is that at least the majority of the stuff, nothing is very computationally expensive. So I don't think we're going to be close on the majority of the stuff. Yeah. I think anything that's like very computationally heavy should go in central.
 
 
00:35:43
 
Alex Del Re: Um but I I don't know like in terms of if you stack I don't know like a 100 different software components onto a palm. What's the resourcing limits there? So that's another thing I'll I'll get a we're not really having a bunch of zones for compute needs. They're doing it more for like just shortening wires and better signals. Yeah, it's like the the ring we were drawing earlier. It's like all about simplifying the harness between the different areas of the vehicle and then the zone is just kind of aggregate all that data that information and spit it out on the bus. There definitely is. Um I don't think we would get away with even besides wiring just throwing everything on one zonal and one central. we probably wouldn't get away with it, but we're not going to be that close to it. And then we're a little over time. Uh just to make sure uh is there anything else we any other questions we have for Ashley right now or Timothy? Sorry. I just wanted to make sure be respectful of their time. Yeah. Okay. I think you guys are good to drop. Go get some lunch.
Ashli Forbes: Okay,
Alex Del Re: Yeah.
Ashli Forbes: thank you guys. How was Wait, how was the torn?
Alex Del Re: Thank you.
Timothy Kyung: Thank you guys.
Ashli Forbes: Was there tornadoes?
Alex Del Re: No, it was a whole whole bunch of up north.
Ashli Forbes: No.
Alex Del Re: They had them, right? Yeah. Yeah. Um where I was Yeah. Where I was it was it hailed, but there was no tornadoes. But the lightning was the craziest lightning I've ever seen. It was like every millisecond it was like I was like, I can't sleep. Yeah. I was like, what the heck is going on?
 
 
Transcription ended after 01:01:39

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
