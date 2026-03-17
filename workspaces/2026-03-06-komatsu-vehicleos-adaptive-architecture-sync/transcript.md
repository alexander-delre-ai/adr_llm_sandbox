Mar 6, 2026
Komatsu <> VehicleOS Adaptive Architecture sync - Transcript
00:00:00
 
Srishti Dhamija: That's these are good questions. Yeah. Yeah. And please definitely like ask questions about the documentation and give us any feedback you have. Uh one thing I can definitely say uh from the uh thread that we had in the shared channel uh page does not model internal application threads at all. So page is I think uh it's restricted to it models things at the process level. Now beyond that uh and a process is just an instance of any particular executable.
Nuthan Sabbani: Okay.
Srishti Dhamija: Now beyond the process level it's completely up to the application developer. Pay doesn't actually explicitly model any threading model and um we don't prescribe any specific APIs either to do like any synchronization or threading.
Nuthan Sabbani: Okay.
Srishti Dhamija: I think that's like completely up to the application developer. But yeah, I'd love to understand your use case and if you have any particular questions. Yeah.
Nuthan Sabbani: Okay. Yeah, sure. Uh I can give you an example.
Srishti Dhamija: Mhm.
Nuthan Sabbani: So as I said uh this payload has like a uh its own main uh state
 
 
00:01:03
 
Srishti Dhamija: Yeah.
Nuthan Sabbani: machine um which and there is a scoreboard
Srishti Dhamija: Yes. Mhm.
Nuthan Sabbani: which uh this state machine calculates a payload meter and it sends to the scoreboard to display
Srishti Dhamija: Okay.
Nuthan Sabbani: on the so that operators will know how much load it is carrying and how much it needs to load for the next uh uh iteration.
Srishti Dhamija: Yeah.
Nuthan Sabbani: So those kind of stuff will be done and at the same time we'll be communicating with the drive
Srishti Dhamija: Mhm.
Nuthan Sabbani: system.
Srishti Dhamija: Mhm.
Nuthan Sabbani: So once uh it it's completed loading and it moves to the destination during that period we we calculate the final load and if it
Srishti Dhamija: Okay. Okay.
Nuthan Sabbani: is if the final payload is more than the rated payload then
Srishti Dhamija: Mhm.
Nuthan Sabbani: it should tell a drive system that okay this driver is carrying uh more than the rated payload. So we have to apply the speed restriction now.
Srishti Dhamija: Mhm. Yeah.
Nuthan Sabbani: So it has to be done from the dry system but the payload will send the information to
 
 
00:02:00
 
Srishti Dhamija: Yeah.
Nuthan Sabbani: it.
Srishti Dhamija: I see. I
Nuthan Sabbani: At the same time it will be displaying uh uh load load lights scoreboard and other uh
Srishti Dhamija: see.
Nuthan Sabbani: indicators uh by communicating to the other controllers also.
Srishti Dhamija: Yeah. I see. I see.
Nuthan Sabbani: So yeah and at the same time uh customers might look at the real time data and uh uh they they'll insert the USB to the controller and they'll collect the data. So to handle all these uh features uh we have like a different threads. One thread is for the main application. Another thread is for the serial communication.
Srishti Dhamija: Mhm.
Nuthan Sabbani: Other thread for the uh CAN communication to send it for the other controllers
Srishti Dhamija: Mhm.
Nuthan Sabbani: sometimes and another thread is for like a hardware IO task which filters the
Srishti Dhamija: Okay. Okay.
Nuthan Sabbani: sensor data. At the same time there is another data service to have all these records and
Srishti Dhamija: Okay.
Nuthan Sabbani: another thread is for getting UI updates sometimes.
 
 
00:03:04
 
Srishti Dhamija: Okay. Got it.
Nuthan Sabbani: So those kind of Uh so uh I was
Srishti Dhamija: Okay, got it. So, yeah. Go ahead. Go ahead. Sorry.
Nuthan Sabbani: going through uh the documentation and uh have like a provider side
Srishti Dhamija: Mhm.
Nuthan Sabbani: of things and consumer side of the things.
Srishti Dhamija: Uhhuh. Yes.
Nuthan Sabbani: um which I understand that okay provider will be uh uh payload application will be sending these information to the other controllers like the drive system and the scoreboard which handles
Srishti Dhamija: Mhm. Mhm.
Nuthan Sabbani: by other zonal controllers and consumer is like uh we get information from the
Srishti Dhamija: Yes.
Nuthan Sabbani: consu uh other zonals uh like the sensor
Srishti Dhamija: Mhm.
Nuthan Sabbani: data and uh how do I send how
Srishti Dhamija: Yes.
Nuthan Sabbani: do I do my application like one thread which which does the main
Srishti Dhamija: Mhm.
Nuthan Sabbani: state machine. How do I tell the other threads?
Srishti Dhamija: Mhm.
Nuthan Sabbani: those kind of things will be handled by the py arch or should I write on my own as I think you said uh I had to handle that part right is
 
 
00:04:04
 
Srishti Dhamija: Yes. Yes. Yes. Uh great question.
Nuthan Sabbani: that
Srishti Dhamija: So um everything you described so out of that the internal threading would be uh handled by the application developer. Uh pyarch doesn't actually model any internal threading within a specific process. What could be handled by pyarch from what you described is the communication between processes.
Nuthan Sabbani: Okay.
Srishti Dhamija: So if you want to um send any data uh you can model different types of communication patterns in pyarch all of which will use some IP at the moment. Um and uh for example for um interhost communication it could use TCP or UDP like you can configure that over some IP and for local communication on the uh same host it would use Unix domain sockets but yeah it's all the sum IP protocol and the communication patterns uh p supports we have three of them it's either you can do event based communication um or like a publish subscribe mechanism Or it could be like a remote procedure call which we call methods.
Nuthan Sabbani: Oops.
Srishti Dhamija: And the third um pattern is fields which is um sort of like remote properties but some shared data that um uh consumers can be notified on like if it changes and also different applications can like access it and also get set and notify.
 
 
00:05:34
 
Srishti Dhamija: It provides those mechanisms. So um yeah so a short answer to your question is internal threading is not modeled but interprocess communication is modeled.
Nuthan Sabbani: Okay. So, inter okay inter application threading won't be uh handled.
Srishti Dhamija: Yes.
Nuthan Sabbani: But uh do you guys have any uh specific design design pattern that you guys want to follow? Uh will you be sharing any any such kind of documentation?
Srishti Dhamija: uh for the applications themselves uh we can share some examples if that's helpful for you like in general uh application development best practices for onboard applications at the moment we don't have any such thing but yeah we'd love to understand uh like what would be helpful
Nuthan Sabbani: Okay.
Srishti Dhamija: yep
Nuthan Sabbani: Okay. I can come up with like a a specific uh use case for you. Maybe we can work on the like an example
Srishti Dhamija: yep yep sure yeah yeah Yeah. Oh, for sure. Yeah. Yeah, definitely.
Nuthan Sabbani: thing.
Srishti Dhamija: We do have some examples on the documentation, but they're not very uh they don't go into all the specific details for maybe your use case.
 
 
00:06:45
 
Srishti Dhamija: So, um if you um just let us know what specific design patterns u you would like um say uh some like guidelines on, we can we can provide more documentation. Yeah.
Nuthan Sabbani: Okay. Okay. Yeah, we'll see into that. Um,
Srishti Dhamija: Yep.
Nuthan Sabbani: yeah. Okay. Hi, Alex. We feel the
Coulomb's Law (SVL-WCAL-HQ, FL3): Hey, hello. Good afternoon everybody slash almost evening for Newton.
Srishti Dhamija: Hello.
Nuthan Sabbani: same.
Coulomb's Law (SVL-WCAL-HQ, FL3): Um yeah, like if there's more uh like step-by-step information or examples we can give you like Newton,
Srishti Dhamija: Mhm.
Coulomb's Law (SVL-WCAL-HQ, FL3): please give us the um kind of like what how you describe the features of payload. like if um if that's kind of what you're focused on,
Srishti Dhamija: Mhm.
Coulomb's Law (SVL-WCAL-HQ, FL3): if you could just list that out, that would help Ashi and her team kind of figure out what we should include in this like reference app for y'all.
Srishti Dhamija: Yeah,
Coulomb's Law (SVL-WCAL-HQ, FL3): Kind of what we did with Irene.
 
 
00:07:33
 
Srishti Dhamija: definitely. Yeah. Yeah, definitely. Yeah. Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): Yeah.
Srishti Dhamija: And and we can iterate over that based on uh what would be helpful.
Coulomb's Law (SVL-WCAL-HQ, FL3): Yeah.
Nuthan Sabbani: Yeah,
Coulomb's Law (SVL-WCAL-HQ, FL3): The goal Yeah.
Srishti Dhamija: Yeah.
Nuthan Sabbani: sure.
Coulomb's Law (SVL-WCAL-HQ, FL3): The goal is have something put into your codebase that you guys can just quickly reference whenever you want.
Nuthan Sabbani: Okay. Yeah, sure. Uh that will be really helpful. Um yeah. Uh Alex, do you have those questions at one place? I not able to find those in the threads.
Coulomb's Law (SVL-WCAL-HQ, FL3): Yeah. Uh, actually like um the adaptive team actually built out built out a like little Excel doc. So I can just pull them up right now. Give me one second. Is adaptive or autosar? Sorry.
Nuthan Sabbani: Okay.
Coulomb's Law (SVL-WCAL-HQ, FL3): And then where are we? Here we are.
 
 
00:08:26
 
Coulomb's Law (SVL-WCAL-HQ, FL3): And then here we are. Oh gosh. Okay. And then now let me know when you can see an Excel sheet and I'll make the font a bit bigger.
Nuthan Sabbani: Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): All right. Uh, is there a question you wanted to focus on,
Nuthan Sabbani: Um yeah, I think uh we got the two one two questions done.
Coulomb's Law (SVL-WCAL-HQ, FL3): Nathan?
Nuthan Sabbani: Uh maybe uh we can start with the question number three.
Srishti Dhamija: Mhm.
Nuthan Sabbani: Uh integrating with the systemd or uh service to your next
Srishti Dhamija: Mhm.
Nuthan Sabbani: one.
Srishti Dhamija: So I'm glad go ahead.
Nuthan Sabbani: Um yeah go
Srishti Dhamija: Go ahead. Yeah. Oh.
Nuthan Sabbani: ahead.
Srishti Dhamija: Uh so I was just going to expand a little bit what on uh so uh what we wrote here. So uh pyarch doesn't explicitly model the service launcher but it'll automatically uh generate the config based on the platform. We support both systemd for Linux and Q uh and SLM for QX.
 
 
00:09:35
 
Srishti Dhamija: And those configs are generated at build time and they would be used to launch all the processes that are defined in bioarch.
Nuthan Sabbani: Okay. So for the system uh we uh as far as I remember we use like a after next parameters in the service files right um if I want my application to start right after
Srishti Dhamija: Okay.
Nuthan Sabbani: the hardware task uh maybe we'll we'll have a um hardware
Srishti Dhamija: Mhm.
Nuthan Sabbani: task as a separate application to filter out the all the sensor data and I want to specify my application has to run only after hardware task is up and running successfully.
Srishti Dhamija: Mhm. Yeah. Yes.
Nuthan Sabbani: Uh if something goes bad with the uh hardware task my application should also kill by itself on on its own and then restart
Srishti Dhamija: Mhm.
Nuthan Sabbani: it back once the hardware task is on. How do we specify that in the batch model?
Srishti Dhamija: Okay.
Nuthan Sabbani: Do you have like any any example to
Srishti Dhamija: Uh I can definitely share an example. So uh how this is modeled in the adaptive system is not specific to systemd
 
 
00:10:42
 
Nuthan Sabbani: show?
Srishti Dhamija: but we uh so what happens here uh with pchain adaptive is that these service launchers will launch the execution manager which is the process orchestrator which will then launch
Nuthan Sabbani: Okay.
Srishti Dhamija: all the other processes. So how you specify startup configurations and all these execution dependencies is in the uh process startup configurations using pyarch and that can allow you to define dependencies between processes and uh I can share
Nuthan Sabbani: It's good.
Srishti Dhamija: an example after the uh after this meeting but uh yeah that's how you would model that in pyarch in the uh process definitions you can specify um state dependent startup configuration is what adaptive calls it and uh u that will automatically get translated to the appropriate configuration for either systemd or QX depending on the platform.
Nuthan Sabbani: Okay. Um, is there any uh I I think it's uh journal control on system D that that uh that monitors all the service files
Srishti Dhamija: Mhm.
Nuthan Sabbani: that got that get executed or like if something goes bad uh a it holds all the
Srishti Dhamija: Yeah.
 
 
00:12:04
 
Srishti Dhamija: Mhm.
Nuthan Sabbani: logging features. Is there any similar kind of thing that you guys
Srishti Dhamija: Yes. Uh good question. So the uh we do have logging for for all the applications which I think currently it goes
Nuthan Sabbani: have?
Srishti Dhamija: to SIS log. I can uh so all the logs are available on board. Uh there's also the execution manager continuously uh logs the status of all the processes in one particular CSV if you want a quick view of the system but uh I believe um I'll have to check on the upcoming features on this like how to query it with the CLI or something but that is not existing at the moment but we do have all the logging in place.
Nuthan Sabbani: Okay. So you mentioned SIS log. It's like only applied only for the service files but not in the application, right? Uh I think it's some some other logger feature available on the applica internal application, right? Is that correct?
Srishti Dhamija: the application logs are also piped to sis log u if uh um we
 
 
00:13:08
 
Nuthan Sabbani: Okay.
Srishti Dhamija: can show I think home.applied applied co as an example uh all the applied applications actually use the ar log module and that also gets piped to the same um destination via the configuration actually that we we have already done that internally. So I can show an example of that as well after this here.
Nuthan Sabbani: Okay. Okay. Yeah. I just wanted to check if it is a similar one or different.
Srishti Dhamija: Yeah. Yes. It's it's similar logs for uh the execution uh manager or the process orchestrator and all
Nuthan Sabbani: Okay.
Srishti Dhamija: the applications are in the same directory.
Nuthan Sabbani: Okay.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Okay. And uh yeah uh so parch process configuration which okay so rules for the startups and resource shutdowns.
Srishti Dhamija: Yes,
Nuthan Sabbani: Yeah that I think that's covered under the systemd one.
Srishti Dhamija: that that would be the same.
Nuthan Sabbani: Okay.
Srishti Dhamija: Yeah. Uh in the same uh configuration we would do that
Nuthan Sabbani: Yeah. Okay. So uh I think uh for the OS selection
 
 
00:14:11
 
Srishti Dhamija: here.
Nuthan Sabbani: part I I couldn't find it on the documentation if it is uh is it uh is it in the examples that you provided in the documentation or it's it's in somewhere else I might have not I might have missed it
Srishti Dhamija: I can double check.
Nuthan Sabbani: somewhere.
Srishti Dhamija: I can double check and I'll also chat with Alex after this about what um like examples we actually shared with all of you and um I can share an example of that as well. I'm noting down the things I should share after this.
Nuthan Sabbani: Okay. Yeah.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Uh so uh I never worked with the Q&X uh directly the does it only use the posics APIs and if some some other APIs uh is is it similar between QX and the Linux?
Srishti Dhamija: So uh posics is definitely supported because portable operating system interface but you can deploy um any C++ applications using any like standard libraries or even third party libraries as long as they're packaged correctly at build time.
Nuthan Sabbani: Okay.
Srishti Dhamija: For example in Yeah.
 
 
00:15:27
 
Nuthan Sabbani: Sorry.
Srishti Dhamija: Yeah. Go ahead.
Nuthan Sabbani: Um uh if if I want to like use a SQL ID uh SQL
Srishti Dhamija: Mhm.
Nuthan Sabbani: database thing,
Srishti Dhamija: Mhm.
Nuthan Sabbani: um how do I integrate that into here?
Srishti Dhamija: Mhm. Uh so that would be uh you would have to set up the proper build configuration and uh so we use basil as our uh build system.
Nuthan Sabbani: Mhm.
Srishti Dhamija: We would have just have to make sure the third party dependencies are defined correctly and uh they are plumbed correctly to any executables we define and um we can take a look at how exactly that's being done but the short answer is it would have to be done in basil in the basil configuration.
Nuthan Sabbani: the computer.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Okay. Is it similar for Linux and Q&X?
Srishti Dhamija: Yeah.
Nuthan Sabbani: Is it is it done in the
Srishti Dhamija: Yes. It's it's very similar as long as in your third party libraries are uh supported
Nuthan Sabbani: same
Srishti Dhamija: for QX uh it should work.
 
 
00:16:24
 
Srishti Dhamija: Uh one example I have is uh our entire platform it uses some IP for communication
Nuthan Sabbani: Oh.
Srishti Dhamija: and uh for we use v the vom IP library for the some IP implementation and we use that on both QX and Linux. So we just bundle that correctly through our system and it works seamlessly across both the platforms. So that's one example of how we do one third party library. But um yeah, as long as it's supported for QX, you can use arbitrary libraries in your application.
Nuthan Sabbani: Okay. Okay.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Makes sense. Um I think so. Once this compilation is done on our local machine,
Srishti Dhamija: Mhm. Mhm.
Nuthan Sabbani: can we I think you mentioned we can use the same executable on both the machines at the same time. uh like is there any particular location that we need to copy it over uh for the different OS
Srishti Dhamija: So, oh, oh, what's the Okay,
Nuthan Sabbani: for the requirement
Srishti Dhamija: I think I misunderstood that question.
 
 
00:17:29
 
Srishti Dhamija: So,
Nuthan Sabbani: part.
Srishti Dhamija: I think what we were answering was we can't use the same built executable. It would have to be built for each target platform. But you can use the same system model after we configure it appropriately for different platforms. You would have to recompile it
Coulomb's Law (SVL-WCAL-HQ, FL3): Yeah.
Nuthan Sabbani: H okay. Yeah, I got confused at at that point.
Srishti Dhamija: yeah know I think I misunderstood that as well.
Nuthan Sabbani: Uh
Srishti Dhamija: Uh but yeah the same system model can definitely be used as long as the platform is configured correctly.
Nuthan Sabbani: okay.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Okay.
Srishti Dhamija: Yeah.
Nuthan Sabbani: So batch model can be s similar for both but the build process could be
Srishti Dhamija: Yes.
Nuthan Sabbani: different.
Srishti Dhamija: Yes, exactly.
Nuthan Sabbani: Okay.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Okay. Yeah, that makes sense.
Srishti Dhamija: And I think this goes back to your question about the OS selection as well. Uh I'll find an example of that and send it to you.
Nuthan Sabbani: Thank you.
 
 
00:18:13
 
Srishti Dhamija: Yeah.
Nuthan Sabbani: Okay. Yeah. Um the answers I'm just noting down some
Srishti Dhamija: Oh yeah, for sure. For sure. Yeah.
Nuthan Sabbani: points.
Coulomb's Law (SVL-WCAL-HQ, FL3): Yeah,
Srishti Dhamija: Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): this one's also being recorded, so it'll have like a transcript and all that.
Nuthan Sabbani: Oh,
Srishti Dhamija: Okay.
Coulomb's Law (SVL-WCAL-HQ, FL3): So,
Srishti Dhamija: Great. Great. Awesome.
Nuthan Sabbani: you're great.
Srishti Dhamija: Yeah.
Nuthan Sabbani: Thanks. Okay. Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): Peace.
Nuthan Sabbani: Uh next one is uh so we get a uh configuration file like configuration setup from the UI.
Srishti Dhamija: Mhm.
Nuthan Sabbani: So right now we have the web page.
Srishti Dhamija: Mhm.
Nuthan Sabbani: Um so system uh hall cycles are in uh in progress.
Srishti Dhamija: Mhm.
Nuthan Sabbani: Um so operator can change scoreboard configuration.
Srishti Dhamija: Okay.
Nuthan Sabbani: Sometimes it could be uh counting down or counting up kind uh those
Srishti Dhamija: Okay.
Nuthan Sabbani: kind of configurations will be changed and the load light uh threshold can also be changed at the
 
 
00:19:11
 
Srishti Dhamija: Mhm. Mhm. Okay.
Nuthan Sabbani: runtime.
Srishti Dhamija: Okay.
Nuthan Sabbani: So how do I design my application to get these
Srishti Dhamija: Mhm.
Nuthan Sabbani: configurations from the UI or from somewhere else?
Srishti Dhamija: Mhm.
Nuthan Sabbani: I think there could be an also an option for loading a configuration file on UI.
Srishti Dhamija: Mhm. Mhm.
Nuthan Sabbani: Uh it can vary uh in future but how do I make
Srishti Dhamija: Mhm.
Coulomb's Law (SVL-WCAL-HQ, FL3): All
Nuthan Sabbani: my application to get those updates as soon as anything changes in
Coulomb's Law (SVL-WCAL-HQ, FL3): Relax.
Srishti Dhamija: Mhm. Huh.
Nuthan Sabbani: there and how do I uh like
Srishti Dhamija: Mhm.
Nuthan Sabbani: prioritize
Srishti Dhamija: Yeah. Uh that's a good question. I I won't have an image answer to like the best uh practice for this particular use case. Uh I would love some more details. But what I can say is that um page doesn't restrict how we design the application. what it it does support some IP and the three communication patterns I mentioned for interprocess communication.
 
 
00:20:16
 
Coulomb's Law (SVL-WCAL-HQ, FL3): All
Srishti Dhamija: So if those three patterns and sum IP are appropriate for this use case then we should use
Coulomb's Law (SVL-WCAL-HQ, FL3): right.
Srishti Dhamija: pyarch and model it within that otherwise we should let the application itself develop
Coulomb's Law (SVL-WCAL-HQ, FL3): s***.
Srishti Dhamija: its own mechanism.
Nuthan Sabbani: Okay. So,
Srishti Dhamija: Yeah.
Nuthan Sabbani: uh if I want to uh have my application to uh process this information,
Srishti Dhamija: Mhm.
Nuthan Sabbani: uh I have like a I created another data service thread on internally in my application. How do I get that configuration file from the UI? is it uh like uh a config file will be stored at some point and I need to go and read that config file to get updated my application.
Srishti Dhamija: Mhm.
Nuthan Sabbani: How do I know that UI is updated this config?
Srishti Dhamija: Mhm. So,
Nuthan Sabbani: Is it like uh so currently I used the like sorry um currently
Srishti Dhamija: uh yeah, go ahead.
Nuthan Sabbani: I use the message QPC mechanism to get any update
Srishti Dhamija: Okay.
 
 
00:21:15
 
Srishti Dhamija: Okay.
Nuthan Sabbani: from web page along with the payload which contains the config
Srishti Dhamija: Got it. Got it. Mhm.
Nuthan Sabbani: that has
Srishti Dhamija: Got it. Got it. So are you looking to change the IPC mechanism fundamentally?
Nuthan Sabbani: changed.
Srishti Dhamija: So and would sum IP work for your use case like in this case is the communication local or is it okay?
Nuthan Sabbani: Uh yeah, it's
Srishti Dhamija: So if sum IP with a Unix domain sockets works for your use case
Nuthan Sabbani: local.
Srishti Dhamija: then we can absolutely use pyarch for this. And one more thing that might be helpful for you as well is the data representation in your application. So I think our docs have some information on this but I can send you some more details. Uh you will pyarch in in pyarch the system modeling starts with your data representations. We support any types that can be converted to native C++ types which would mean all primitives, strings, arrays, vectors, maps, variants as well, uh, enums as well.
 
 
00:22:22
 
Srishti Dhamija: Um, so strrus and if this is a convenient way to model all the data and and sum is an appropriate communication mechanism. In this use case, if a communication is local, it would use Unix domain sockets. If that's appropriate, then we should use Py. Otherwise, yeah, we can evaluate like P doesn't restrict the IPC mechanism. It just Yeah. So I mean yeah um uh in my short answer is I think I'm trying to give options of
Nuthan Sabbani: Okay.
Srishti Dhamija: what pyarch provides but I think I would have to understand the use case a little better to um
Nuthan Sabbani: Wait.
Srishti Dhamija: give any more guidelines on like what the best u like way forward would be here.
Nuthan Sabbani: Okay. Uh I'll try to explain it in the in detail.
Srishti Dhamija: Okay, sounds good.
Nuthan Sabbani: Um uh so when a hall cycle is in progress as I mentioned
Srishti Dhamija: Definitely. Yeah.
Nuthan Sabbani: um it calculates a payload and it displays some data
Srishti Dhamija: Okay.
Nuthan Sabbani: on the scoreboard which is like we call it now a countdown like uh
 
 
00:23:22
 
Srishti Dhamija: Okay. Okay.
Nuthan Sabbani: this uh so ra uh if it is carrying less than uh uh uh retail payload it will just display the
Srishti Dhamija: Okay.
Nuthan Sabbani: uh how much remaining how much the differences you can uh load on
Srishti Dhamija: Okay.
Nuthan Sabbani: the screen uh which is based on the previous configuration done by the
Srishti Dhamija: Okay. I see.
Nuthan Sabbani: user on the UI.
Srishti Dhamija: Okay. Okay.
Nuthan Sabbani: Now user decided to go with uh change it to count
Srishti Dhamija: Okay.
Nuthan Sabbani: up it. Uh now the scoreboard has to uh display how much load is loaded on the
Srishti Dhamija: Mhm. Okay. Okay.
Nuthan Sabbani: truck instead of the remaining load.
Srishti Dhamija: Yeah. Yeah.
Nuthan Sabbani: So once he gets uh he updates on the UI,
Srishti Dhamija: Mhm.
Nuthan Sabbani: I need to get that information to my application and immediately I have to update the
Srishti Dhamija: Mhm.
Nuthan Sabbani: scoreboard.
Srishti Dhamija: Mhm.
Nuthan Sabbani: I'm asking like right now I'm only thinking that uh I use I will use the message Q
 
 
00:24:26
 
Srishti Dhamija: Okay.
Nuthan Sabbani: once the UI gets updated I'll get a uh event like hey this is updated
Srishti Dhamija: Mhm. Yeah. Mhm.
Nuthan Sabbani: you have to update your uh function to display this this one.
Srishti Dhamija: Y Okay.
Nuthan Sabbani: So that that's the use case.
Srishti Dhamija: Okay.
Nuthan Sabbani: I
Srishti Dhamija: Got it. So,
Nuthan Sabbani: have
Srishti Dhamija: it sounds like this is like periodic data where you don't need a response back. Is that right? Like you Okay. So,
Nuthan Sabbani: yes uh I have my own I have a thread which polls
Srishti Dhamija: then Yeah.
Nuthan Sabbani: every 50 milliseconds to get uh to read any data coming in from
Srishti Dhamija: Okay. Okay.
Nuthan Sabbani: the web
Srishti Dhamija: Okay. Okay. So,
Nuthan Sabbani: page.
Srishti Dhamija: I think uh some IP events would be uh pretty appropriate for this if you just want to do like oneway communication without a response. And we could even use methods the RPC mechanism I described earlier which would uh allow you
 
 
00:25:09
 
Nuthan Sabbani: Mhm.
Srishti Dhamija: to get a response back. And the response how methods work is you can do some remote procedure call and get a future back. uh and when the response arrives the future will complete and you can uh elsewhere in your application query the status of that future and do some continuations on that or yeah or just keep polling. So that is important and I think both of these might be appropriate for your use case.
Nuthan Sabbani: Okay. Okay.
Srishti Dhamija: Yeah.
Nuthan Sabbani: So that does it also brings the payload like what the config that has changed that information structure.
Srishti Dhamija: Uh so in yeah you can uh process like you can define arbitrary input and output arguments for a method and that's completely user defined and configurable.
Nuthan Sabbani: Okay. Okay. Yeah,
Srishti Dhamija: Yeah.
Nuthan Sabbani: it's good. And you mentioned it's unique domain socket. Is it a similar one from uh with
Srishti Dhamija: Yes.
Nuthan Sabbani: some
Srishti Dhamija: Uh so Unix domain sockets are one layer below sum IP.
 
 
00:26:26
 
Srishti Dhamija: Sum IP is the protocol.
Nuthan Sabbani: Okay.
Srishti Dhamija: Uh VMIP is the implementation we use and underneath VSIP it uses like lower level transport mechanisms depending on uh whether you're communicating on the same host or not. If you're communicating on the same host it'll use Unix domain sockets which are uh essentially uh file descriptors. It's just high performance data exchange between um like processes that are on the
Nuthan Sabbani: Amen.
Srishti Dhamija: same host and um the advantage of Unix Roman sockets is they completely bypass
Nuthan Sabbani: Okay.
Srishti Dhamija: the network stack. So you don't need to go through um you don't need to do for example even local even local host goes through the entire network stack and back
Nuthan Sabbani: Listen.
Srishti Dhamija: which is what Unix domain sockets will completely by bypass like for example the loop back interface uses the entire network stack which won't happen if you use a domain so Unix domain socket but uh all of this detail is actually abstracted away from the user so visip automatically chooses a unique domain socket or TCP uh or UDP depending on like where the data needs to go.
 
 
00:27:39
 
Srishti Dhamija: There's no special configuration required for that. It just automatically chooses the most efficient way to transfer data.
Nuthan Sabbani: Okay. Yeah, understood. Yeah,
Srishti Dhamija: Yeah.
Nuthan Sabbani: I would love to read about this some IP. I'm pretty uh new to this topic.
Srishti Dhamija: Yeah. Yeah. Yeah.
Nuthan Sabbani: Good.
Srishti Dhamija: It's interesting.
Nuthan Sabbani: Okay. Yeah. Uh thanks. Uh uh I think uh next questions are covered again.
Coulomb's Law (SVL-WCAL-HQ, FL3): Uh I guess before we go forward is we're like at the time we allocated for this.
Nuthan Sabbani: Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): Um, are is everyone okay to stay a bit longer or um should we maybe restart this on Monday during office hours?
Nuthan Sabbani: Uh I think I have I have only one question I can stay for like I don't know five minutes.
Srishti Dhamija: I'm happy. Yeah,
Nuthan Sabbani: Is it okay for you guys?
Srishti Dhamija: I'm happy to stay back as well.
Coulomb's Law (SVL-WCAL-HQ, FL3): Okay,
Srishti Dhamija: Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): cool.
 
 
00:28:35
 
Coulomb's Law (SVL-WCAL-HQ, FL3): We'll stay then.
Srishti Dhamija: Yep.
Coulomb's Law (SVL-WCAL-HQ, FL3): Yep.
Nuthan Sabbani: Yeah.
Srishti Dhamija: Yep.
Nuthan Sabbani: Okay. Uh so I think uh eight and nine all also answer uh persistency is
Srishti Dhamija: Mhm.
Nuthan Sabbani: uh something I'm interested uh yeah uh the 10 is good uh so what what I mean about the 11th schema migration handle is uh uh so we had a uh a request from customer back uh some time ago um we were giving out the hall cycle records in some for only some uh parameters and they requested for an additional parameters for the next software update.
Srishti Dhamija: Mhm.
Nuthan Sabbani: So we had like a a database file uh which we read for every like after software updates or uh each power cycle we read from the uh database
Srishti Dhamija: Mhm.
Nuthan Sabbani: file and uh we get the what are what are the data that we were running before
Srishti Dhamija: Mhm.
Nuthan Sabbani: the shutdown or software update. So when we updated our function to add this new
Srishti Dhamija: Mhm.
Nuthan Sabbani: feature the data we when we read is different from what the
 
 
00:29:48
 
Srishti Dhamija: Mhm.
Nuthan Sabbani: what the structure we have it in the uh in the application. So it gets corrupted right because the structure is uh different from what we are
Srishti Dhamija: Mhm.
Nuthan Sabbani: reading. Uh so at that situation we had to like delete the old uh uh database file create a new one adding this new column in there uh those kind of stuff it was hard to maintain uh at some point
Srishti Dhamija: Mhm. Okay. Mhm.
Nuthan Sabbani: uh persistency can handle th those kind of situation like uh if I know you can store like a a key and a value I want to make my the uh value part uh
Srishti Dhamija: Yes.
Nuthan Sabbani: into like a big structure and the key part uh will be
Srishti Dhamija: Okay. Mhm.
Nuthan Sabbani: staying safe uh same uh the uh value part will be adding the big structure
Srishti Dhamija: Mhm.
Nuthan Sabbani: with a version uh different version of a
Srishti Dhamija: Mhm.
Nuthan Sabbani: structure.
Srishti Dhamija: Okay.
Nuthan Sabbani: So how do you guys handle it in such situation?
 
 
00:30:56
 
Nuthan Sabbani: Have you guys worked on such scenarios?
Srishti Dhamija: Mhm. I'll have to look into that. Uh I'm not very familiar with the persist persistency module, but uh I'll look into that and get back to you. Yeah,
Nuthan Sabbani: Okay.
Srishti Dhamija: I have other folks on my team who build that module out,
Nuthan Sabbani: Yeah.
Srishti Dhamija: so I can ask them and get back to you. Yeah,
Nuthan Sabbani: Yeah. Yeah. That's what I mean in with the schema migration like if structure gets updated with the
Srishti Dhamija: got it. Got it. Yes. Yeah. Yeah. Yeah. I understand.
Nuthan Sabbani: new
Srishti Dhamija: Uh I understand the problem. And now we need to do uh like version handling uh within the persistency module. So um I I'll look into that whether that's supported and yeah I can uh help answer that maybe next week. Yeah.
Nuthan Sabbani: Yeah, because uh for the payload meter application uh hall cycle is like a very important thing.
 
 
00:31:39
 
Srishti Dhamija: Mhm. Okay.
Nuthan Sabbani: Um so uh if something goes bad and application gets uh
Srishti Dhamija: Yes. Yeah.
Nuthan Sabbani: restarted it has to know where it was before the power cycle and has
Srishti Dhamija: Definitely. Yeah.
Nuthan Sabbani: to resume from there. If some uh after the software updates if something goes changes uh we still need to uh read the
Srishti Dhamija: Mhm.
Nuthan Sabbani: old file.
Srishti Dhamija: Mhm.
Nuthan Sabbani: If if something is different then it will just get corrupted and the application would crash.
Srishti Dhamija: Yes. Makes sense. Yeah. Yeah. Um yeah, I I'll look into that for sure and and get back to you.
Nuthan Sabbani: Yeah.
Srishti Dhamija: Um anything else I can help answer right now?
Nuthan Sabbani: Uh I think uh that's a major question.
Srishti Dhamija: Okay. Okay. Okay.
Nuthan Sabbani: Uh I think the 13th is also answered.
Srishti Dhamija: Mhm.
Nuthan Sabbani: Uh 12th, yeah, it's not supported. Okay. Yeah. Uh that's all I have for now.
 
 
00:32:32
 
Nuthan Sabbani: Maybe uh oh uh one more thing is uh Alex I I want to get started with the
Srishti Dhamija: Mhm.
Nuthan Sabbani: uh development part for the adapt just to get a hands-on experience like work on some demo um just like we did for the classic auto
Coulomb's Law (SVL-WCAL-HQ, FL3): Yeah. Uh I think if this was kind of what we were talking about at the beginning,
Nuthan Sabbani: set
Coulomb's Law (SVL-WCAL-HQ, FL3): if you have more specific if you can give us like a list of specific needs you want for like a demo or walk through a reference application um we can build out that documentation. That being said, it will take you know some time to kind of like aggregate and format the
Nuthan Sabbani: Okay.
Coulomb's Law (SVL-WCAL-HQ, FL3): info.
Nuthan Sabbani: If I follow the uh steps that you guys have on the documentation, would I be able to uh de develop like my own uh demo
Srishti Dhamija: You should definitely Yeah,
Coulomb's Law (SVL-WCAL-HQ, FL3): I think that's No,
Nuthan Sabbani: project?
Srishti Dhamija: go ahead. Go ahead.
 
 
00:33:22
 
Srishti Dhamija: Sorry. Yeah.
Coulomb's Law (SVL-WCAL-HQ, FL3): no, you you're the expert. You got
Srishti Dhamija: Oh, no. No, no. I was just saying you you should definitely be able to build out all the uh different uh
Coulomb's Law (SVL-WCAL-HQ, FL3): it.
Srishti Dhamija: like modeling pieces. we def uh we step through how to do like data types then service interfaces for communication uh executables machine and deployments that's how we step through the modeling tutorials and then I think we have some tutorials on doing the application development specifically as well uh that those are not very prescriptive because they are uh on a complete different use case so uh but you should be able to get started with that and build out a structure and have something working but yeah once We have that we can provide more details.
Nuthan Sabbani: Okay. Uh is something that we need to uh you guys need to update on our repo uh kon repo uh to get this
Coulomb's Law (SVL-WCAL-HQ, FL3): Uh,
Nuthan Sabbani: started.
Coulomb's Law (SVL-WCAL-HQ, FL3): I'd have to check to I'll check with the team or I'll put an action in to check with the team to see if all the dependencies are there in the katana repo.
 
 
00:34:26
 
Coulomb's Law (SVL-WCAL-HQ, FL3): Um, if they aren't, it should just be a simple uprev that we can um that we can put on the on out to you
Nuthan Sabbani: Okay.
Coulomb's Law (SVL-WCAL-HQ, FL3): guys.
Nuthan Sabbani: Yeah, I think I think that would be good uh for now. Uh maybe I'll once I get started with this, I might come up with more questions and then we can discuss in the office
Coulomb's Law (SVL-WCAL-HQ, FL3): Yep. Yeah. Yeah,
Nuthan Sabbani: hours.
Coulomb's Law (SVL-WCAL-HQ, FL3): I think like um uh I think the best step forward is for you to work through the tutorials we have online and then um any uh trips or issues you have like post on the
Nuthan Sabbani: Mhm.
Coulomb's Law (SVL-WCAL-HQ, FL3): channel kind of like what you did for these questions and then we can work through them together have an ad hoc meeting or
Nuthan Sabbani: Sure.
Coulomb's Law (SVL-WCAL-HQ, FL3): talk through it through office hours. Yep.
Nuthan Sabbani: Thanks.
Coulomb's Law (SVL-WCAL-HQ, FL3): All right. Uh there's something else I'll uh I took a good amount of notes also.
 
 
Transcription ended after 00:37:15

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.