SDV SIL Testing-20260317_111420-Meeting Recording
March 17, 2026, 4:14PM
2h 50m 5s

Joseph Boyer started transcription

(PMO-CCLL-B-Iron)   0:04
So let me share my screen.
And So what is sill so sills like this overarching term of software and loop, so thinking about.
The tests you guys are writing in your code base for each one of the apps that you're looking at.
That is a version of Sill, but it's a very narrow scoped version.
I'd say it's like we talked about a bit before like this is what I would say like is more the unit test unit test focus for each one of your software.
Components.
But we're talking about when it comes to Workbench is more integration level testing.
So when we say SIL.
When I say Sil, I'm talking about what's gonna happen when we have autolube running payload running and whatever else you guys wanna have on the truck.
And how can we assess?
Let's say for auto loop, how can we assess based on the signals that we're getting in, say, machines functioning correctly? The downstream signals are getting sent accordingly.
Does that distinction make sense to you guys?
OK. And an idea, I think I after talking in that hill meeting, we had the other day. Sill is kind of gonna replace or ideally replace a lot of the initial signal validation or an IO checks that you guys do as part of your hill testing I mean.
I don't think it'll completely replace, but it'll be.
A way for you guys to assess before you actually put Dakota hardware.
And that's that's still test this like full system zone to zone.
Communication.
Like from input all the way through a ring to another zone to an output.
Yeah. So in SIL, we have these things called virtual Ecus or virtualized representations of each one of the different.
Components.
And as well as the interfaces between.
So depending on like the scope of what you're trying to test, you can define whether it's yours, the zone for the app that's running the other zones.
Or like whatever meets your sandbox criteria.
OK.
And like the idea of the great thing with syil is that you guys can like more rapidly test, you know, having to constantly flash. You can kind of update your scripts.
In the repo repo Docker image and I quickly test on Workbench.
Any questions on this before I talk about virtual ECOS?
OK.
Going into these so virtual ECU is essentially A framework that we like.
It's built a framework built into vehicle OS that allows you guys to bring up a sill incense that represents your target system.
So these virtual ECU's you can kind of think of them as like, you know like doctor Containers running on your your cluster or your code servers.
You're.
That kind of represent your one of your zones, or Maple or walnut or juniper or whatever compute you're trying to think about. And these virtual virtual Ecus can be either firmware or cannot run either firmware or autos or applications.
That kind of goes into how you define what we call the compute element in this case, so the compute element is what essentially describes what your virtual eco is gonna look like, and there's one down here that I'll show you in a little bit, but looking at like.
Bringing up the virtual environment, you can.
Think of this as a way of once you have your syscoms defined and your compute elements defined as well as all the networking configuration, all that created, you can simply.
Start your virtual ECU instances with like a MAZ command and MAZ is essentially just like a a shell script we have in our vehicle OS container or the Cortana container in this case.
I think I know like a very high level covering virtual Ecus.
Any specific questions I can try and address?
Right now.
Have you guys worked with virtual ECOS before?
Roughly, I'm gonna imagine setting these ECUS up is a applied domain if a year down the road we decide we need a fifth stone.
Be.
Or I guess two years down there whenever.
The maintainability would be on the applied.
Front right.
Yeah, I mean that's an open question I have with the team right now is like ultimately who owns the virtualization, the definition of the virtualization of all these elements because you guys are working with like.
Pom and then Juniper hardware for your zonal architecture, we're gonna be drafting or developing what those sys comps will look like.
So it'll be very much us working in tandem on like those definitions.
And it I've seen syscom's a bunch.
Are you guys familiar with that?
OK, I'll note that for a little bit.
Essentially, the syscomp is what defines.
Like the system composition, essentially what defines what is in your electric or your vehicle architecture and how it all communicates with each other.
Yeah. So actually, maybe we can just talk about a sys comp right now because.
That is what I want to show next, at least an example of a compute element that one SEC.
Yeah, actually, let's just go through the docs. Then we can kinda talk about it from there.
So what do you call it?
There is like.
This fundamental or this building block we call this mosaic compute element.
This is like the basic building block that defines what a single compute node will look like and essentially says what is the hardware that I'm trying to target and how can I connect to it with my with my specific software components.
So you can see here in this QEMU QQQ.
I've actually never said that acronym out loud.
Anyways, in this Docker container like this is essentially us. We're trying to represent or virtualize central compute.
This is.
So you can see the name, you can see the build target for what we're trying to create.
It's Qualcomm, QNX for Torrent central, and then whatever build flags you might need and then down here is like you can specify.
What the interfaces are so like what?
What is this gonna be connecting to the greater vehicle us on in terms of what the interface is called?
It's EMAC in this case.
And then what is the IP? So on and so forth and then the the rest of the Rs are kind of like how to set it up?
What environment verb is you wanna you wanna include?
How to how you can SSH and log into here? A lot of these extra or these other commands or other details are used by downstream processes such as OTA such as enabling you guys the ability to SSH.
Into the specific virtualized container or when it's deployed in the vehicle, SSH into the compute element on the truck itself.
But high level or big picture, this is kind of how we define what is going to get virtualized and how we can talk to it.
To get the majority of the magic is in that Qualcomm QNX file.
Yeah, I mean this is the build target.
So in the case of Qualcomm Q&X, this is pulling the Qualcomm source binary in this case and having that run in this key.
I'm gonna call.
I'm gonna queue queue, queue, queue.
Oh God, I can't say it, but it's that's what runs on this this container.
Is that something provided by Qualcomm?
But it it is provided by Qualcomm, but I know there's some NDA going about that Josh is working on.
Yeah, I I'm curious if this is like if you get how much work you guys are doing behind the scenes to make this work or how much it's provided from the supplier?
So there's a couple different path.
A few different pathways there.
The first is like the supplier likes us and is willing to work with us and play ball. They give us the binary.
It's very easy to run.
Sure, we can just load it directly on the second is we can work through.
A customer in this case.
Like Komatsu, so you guys have a good supply relationship.
We can get the binary that way.
There's some permissions there if, like they won't explicitly let applied see it, but we can get around with third party dependencies and then third if.
The supplier doesn't like applied or doesn't like you guys for whatever reason.
Or they just are scared about privacy.
We have to reverse engineer.
Like what?
That build target would look like.
So I'm imagining there's gonna be a mix of all three of those when it comes to actually building.
Your sys comps.
OK.
Alright, so this is what like what it looks like for like a mosaic or sorry, a central compute element.
The next is like for like a yocto or lighter version that we would run that we build to run firmware.
Same exact thing, it's just.
Rather than looking at.
The QNX, we'll target it.
We're looking at this like smaller Linux X86, and we're talking about this for, but same exact kind of package here.
The thing that connects these two together is that what we call.
A virtual ECU config so you can kind of think of this as what defines how these two different compute elements are gonna talk to each other.
So in each of these containers we we list out what its name is the IP address.
And then specifically what this start script is, so when we build up these different VCU's you can think of it as just like a big Docker compose.
So starting each one of these containers separately.
With different build arguments.
Are you guys familiar with Docker compose or Docker containers in general?
So like when you run a docker container, there's like this, typically like a Docker start file and that start file has a bunch of environment variables and other specific configurations for that container that defines how it gets brought up.
So that's what these start scripts are doing.
So.
So if you wanted to customize the central bring up based on some specific truck configuration or some specific like user access level or.
What are other common ways to configure the the container?
Typically it's just for like truck configuration or something like that, but like if you wanna, that's how you could do it with a start script.
So I imagine as you guys start building out your definition for the ninthirtye for the first kind of.
Lap of development, I'd say.
This is like the script.
This script is where you can play around into configure that. Any questions there?
Those configurations, accessible as part of like our sales scripting or is that we have to have a a sys comp for this config and a sys comp this config.
So the syscomp is like the like what we're looking at right now goes into the syscom like so this is when we look at a real file, it'll be in the syscom.
So.
The start scripts I think can be configurable based on like if you set like an environment file or some sort of build variation there.
So I'll have to that's a question I can talk about with the team.
What was the second part? Sorry.
I was just curious what.
Avenues we had for testing multiple different configurations. Just what that would look like with.
Yeah. So like runtime, like we're still working on getting a solution out for your team. I've been talking about that with the core platform guys, but this like these different start scripts would be how you would start a different.
Sill testing environment for different configurations of your trucks, so you can think of you would have like these would be defined in the Cortana repo or whatever repo you want and this would say.
Start for 9:30.
Start for 830, start for shovel, start for LHD or whatever it might be.
So.
Yeah. And then within those, there might be different build targets or whatever, but like those can be encapsulated in the start script and then also the compute element.
Any questions on this before I keep going?
So we think about we define all these different elements, these different vectors.
Oh, sorry. Before I keep going.
There's like another version of these different of virtual ECU.
So rather than thinking of it as like a full representation of this like heavy.
What do I call it?
Like chemo's, like a pretty heavy virtualization of like it does, like the whole firmware or sorry the whole OS and but if you wanted to do something a bit lighter, maybe more presenting like an embedded app. In this case you could do what's called a Docker virt.
ECU.
And that's essentially just like a lighter version that you can use to run from our applications.
Does that make sense?
OK.
Enough, enough.
Yeah. So, like we think of like Q&X as like very heavy. And then in this case, the way I'm interpreting this is like the virtual ECU for Docker is lighter.
So if you're doing more payload.
Testing you would do both Q&X instances to kind of get more realistic communication between payload and the downstream zones.
But if you were just thinking about revving on auto Lube and not really worried about.
Fully recreating.
Or I forget the different levels of virtualization, but fully virtualizing central rather than just like you can just step out the signals. That's where this.
Lighter Docker virtual config would come from, yeah, Yep.
OK, so looking at the network architecture, this is a bit opaque, but the idea is this is a set of Docker containers that are gonna be running on a network running on your machine.
So typically when you start up a Docker container set of Docker containers, there's some internal network or local network running on your machine that defines communication between the two of them.
So in this case, when we're talking about.
An external network.
This just means the Docker bridge network.
How are we gonna bridge all these different docker containers? All these different VECUS together?
Our container.
So once we have that network identified, the next is looking at what?
How can we bridge each of these together?
So, like what's the port?
What the what's the way we can kind of have these talk to each other in this example or in this this discussion.
It's like we're using Ethernet to define. We're gonna have a port that we're gonna have.
Virtualized that little connect each one of these containers that those would be those IPS we saw in the.
Compute elements, so once we have the IPS defined, this is used by the bridge interface to actually have them talk to the.
The what do you call the virtual machine or the VM in this case and this essentially?
What's super familiar with this?
But this is like essentially just like a Linux bridge that defines.
Or pipes the network commands to the VM and that's via what I just learned is a tap interface.
It's essentially just like a network switch in this case, so starting from the the network, we define the IPS for each one of these, VCU's those go through some Linux bridge or this bridge interface.
There are routes. All these different IPS together and then assuming we find one that matches our central compute or our front zonal that goes through this network, switch to the VM itself.
Generally makes sense to you guys or any questions there.
I think like this is this architecture will apply to like. However you define your veces.
But where you will customize how they will talk to each other will all stem from this.
ECU config essentially.
And so.
When it comes to actually like building all of these, like virtualized containers or sorry virtualized dcus, it's a matter of just running a few different.
Build scripts.
So essentially you get a run of build script for each one of the zones that you want to create, and then once those.
Are.
Built. You can go through these.
What do you call it?
These commands kind of ensure they're running correctly.
Check their status and then execute some of your tests.
But we have separate build scripts read zone.
Alright, the zone will build script that's run multiple times.
Zonal build script read zone.
Sorry it.
All these zones ECU wise are the the same.
If from an ECU perspective they're the same and they have the same targets and they're running.
Like hardware configuration.
At the same.
The hardware's just the same.
Let me think.
Yeah, theoretically the build will be the same.
Yes, and you can reference that.
Where is it?
Generate multiple instances of the same build.
You would reference that.
I can see you config I think.
I'll note that question down like where to reference.
It's like local dev ring name.
'Cause, like essentially the syntax of this is OOP, Tomoko talker. The syntax syntax of this is like we run the compose command, which is essentially a way to bring up multiple containers at the same time. Building according to this compose YAML, and this is the target we're trying.
To build towards or the name of the the rig that we're building for.
So in your case, caps on all.
And then if you wanna rebuild, I guess more narrowly like the specific key.
Image or whatever else this is like where you can do that as well.
OK.
So this kind of covers a lot of like the virtual ECU creation. I encourage you guys kind of like read through this.
And.
Let me know other questions that you guys have or we can talk about them now.
OK.
We'll have questions later.
Yeah, I imagine so.
Just to reiterate, this is applied.
We'll be building these files and we'll basically just be running them right.
Or are we in charge of building the sitcoms?
So we will be building the Syscom set first. I think the big part where you guys are gonna be playing a role in is defining.
Where are we fit fitness?
You mainly you guys are big consumers of what we're talking about right now, but I just wanted to make sure you guys got a sense of like.
The architecture here, sure, the big part or you guys gonna be involved in is like this start script definition.
It's like, how are we gonna actually define how these boards will get brought these boards?
Get product.
OK, OK.
Alright, so the next part is.
These docs I guess are less interesting and I would I would say, but essentially this is how we can define specifically for adaptive or for firmer applications.
How can we start to do testing on them but?
There's not too much detail here in here, but the idea is you define your system composition or the sys comp that I was talking about before.
You orchestrate your rig, which is essentially saying.
Let's build a version of this rig, and when I say rig, that's capsul. In this case, it's a target that you're trying to build towards and let's deploy it to some virtualized instance and start it.
Incense started.
So thinking about.
The the commands we're looking for for VCU's. This is another way to kind of get that network created and this is how you can then run tests, assuming everything starts up correctly, you can just SSH into the board and like do what you want, do what you.
Want to do?
Or just inspect it but.
This is how you would actually run those app like in autosar or products application.
And all that which applications it should be running is identified and deployed in the start script.
Where is it I guess?
How do we tie this ECU to then our target and like our all of our prior definition stuff?
I guess where does it tie into our?
Repository target.
The empire's defines.
That's a good question.
Just 'cause. I've named it cabs normal.
Now how do I get it to do all the cabs normal things?
Hmm.
Noting that question down.
Business simulating all the middleware components as well.
Yeah. So like all the all the middleware, all the interface that'll out come to find out they get they talk to each other.
So in your case it's gonna be signal gateway to the Ethernet bus to Edu to can.
That will all be all.
That all all those other components we brought up based on how the SYS comp is defined, OK, so yeah.
So the next thing I want to talk about is.
Like testing with a signal probe so.
A signal probe is a way for you guys to kind of track a better word, probe your application.
It's a story you can say. All right, I want to monitor door state or I want to monitor auto loop pressure or whatever it is. And this is how you can build out that instrument in your application to monitor that information.
So essentially what that looks like is in pie arch.
You will say I want to import this given for door.
Let's look at the doorstep example. I want to monitor.
Oh, what's going on here?
What's going on here?
We're back.
Monitor doorstep.
The doorstep.
We define what was called this signal probe executable and then when you are defining.
We define what was called this signal probe executable and then when you are defining.
The signal. Sorry, the door state controller or the door state interface you add in.
The signal probe there.
Does that make sense, everybody?
Storage interface has to be unique.
You can't reuse interfaces for multiple inputs.
Sorry I arch so each pyarge interface has to be unique.
We can't reuse interfaces for multiple input signals multiple output signals.
When you say like unique you mean for like auto loop you have a set of signals that you want to ingest, but you're saying there can be some child interface or some.
The bottle lubes.
The sorry there's like some parent interface to autoloop that's trying to say. These are like common signals we wanna talk to.
Can we just refer to that or are you saying does the interface need to be explicitly defined for each case?
So if I have two different auto loop controllers depending on a configuration.
And I initially I was planning on just defining the interface to the manager that the.
That each controller should have.
That would mean.
Or at least be provided poor and if I'm sending out information and I want to.
Find required interface I if we're using the pie arch interface for it to find the signal probe, what happens if that interface is used in multiple locations?
Does that make sense?
Reply.
If you're using the same interface in multiple locations, yeah. Can you monitor like, how is the signal probe get replicated or duplicated in this case?
It's more how does? How does this know where to find her?
I think we actually found that you cannot have.
To require an inputs or two provided.
Required porch or two provided ports using the same interface object.
So I think that is part of it.
I.
I don't know the answer to this, so I just wanna like note the question down accurately.
So you're saying like, how can you ensure your signal probe when it's defined in the same interface, can talk to?
Sorry, can you reiterate the question?
I'm trying to like figure out how to word it.
I.
Feel like it would be easiest to graph it.
Marcus, that was a thing question last time.
Yeah.
You want to draw it out or do it on mirror.
Actually, I'll bring up the mirror from.
Discussion made earlier.
So.
You're discussing with Ashley?
We.
I believe we decided that it was gonna look more like this.
Where this?
Check component in the middle.
It's still being worked on of knowing.
Which to route.
The problem in my mind, at least with this and now that I'm thinking of stuff that we've seen, lies where we define those interface piarch components.
Bring up stuff if we want. So if we define.
An interface component on the manager side that gets consumed by both controller A and controller B, and both of these are running in real time on it, even though they might not be linked properly through this.
How does it know?
Like which one?
Will it know which one to look at?
The signal probe.
Yeah. So or.
Will we even be able to do that with this configuration check? I think we're gonna break a pie arch thing requirement, but.
So the signal probe needs to be defined for each one of the interfaces you wanna look at.
So you will have to have like a separate probe for like A to configuration check B to configuration check and then check to manager.
Yeah.
So that would mean that we need a separate interface variable for each of those.
Separate interface for each of those is.
I think.
No, I I see what you're trying to say.
It's like in our.
This is.
Simple.
Their interfaces we define like what?
The interface variables are that are between controller and manager.
So if we have multiple controllers that are using the same interface definition, we're gonna be using the same interface variables.
Et cetera.
And then software came on it.
You would pull in that interface from the manager.
And this is that same.
This is the same poll you're doing in signal probe right where you're pulling these.
Variables.
Definitions and finding out where they're used in code, I'm guessing is what's happening behind the scenes.
And your concern is like, how do you make sure we're having it?
Look at specifically these signals.
Or whatever. Yeah, yeah.
They're.
They're tied to two different controllers.
Components in general.
I plan on having like defining the interfaces for like for example we have engine running.
Right as a as a.
As a thing, it'll be consumed by a bunch of different.
Things.
And that example.
They're all the same, but what happens if it's being provided from more than one spot?
So say we have battery in an engine, right?
It's running, but our configuration is telling us that only our engine, our battery, should be running.
OK.
Right. Both are gonna be saying powertrain state, but based off the configurations, we're gonna trust one of those.
Right in the code? Yep.
Is that gonna be a problem?
With this, if we're just grabbing from the interface, do we have to have separate interfaces definitions for engine, powertrain, running versus battery, powertrain, running?
Not.
Think I would want to use the same interface variable for both of those.
It's a better example.
That makes sense.
So it's like, how do how do we make sure which interface is gonna be used for?
I guess which interface we're gonna be looking at probing against.
Yeah, because I think given a configuration in this case.
This hasn't been a problem in the past because your build.
All of your configurations have been on the build side, which means that those interfaces are actually only ever used once in the code, but now they'll be used multiple times.
But we'll just be deciding which ones to.
Look at and which ones not to.
So I guess I just wanna make sure that this.
CIL can do the same thing.
So I guess historically you guys have been able to kind of from the test setups or the hill setup you showed me, it's, yeah, you guys have been able to monitor however many signals you want based on what you're trying to test.
So the concern here from your side.
Is.
How heavy is the lift to define what?
How can I like the goal for you? Son is like, how do I watch every watch? The signals that I want to consume. But upstream of that, there's gonna be different configurations or different.
Setups and you wanna know if you need to create. I guess additional probes or additional.
Interfaces to.
Monitor those.
I'm concerned that we're gonna run into issues just that you guys are gonna run into issues implementing this with the.
Runtime configuration stuff that we're.
Just looking at this by using these interface variables as your.
Hook.
So maybe if it works it works, we can.
Yeah. I mean, I think this is something.
We could pop out with Ian seeing from the pie outside.
If you have a better sure way to maybe articulate.
Or provide feedback to what you're saying, sure.
No, no, I this is like, these are good questions.
Should take back.
Umm.
Alright, gotta reshare.
Yeah. So what thinking about the signal probe noted a whole bunch of questions and from like the interface side, how can we actually make sure that this is gonna get applied across different configurations and different interfaces? You guys are looking to to create?
If what you call it.
From the code generation side, you know.
Signal probes different, different from other executables.
Is that like you need to specifically load in the signal probes role so that it knows to visual in.
This information.
Like you can think of like as a mental model of you have like some service interface. You have some executable and we need to build that executable. The signal probe in order for everything to talk to the manager.
Or sorry, talk to the interface.
Yeah, like a signal probe is in effect like connected to the entire interface that you define and will have knowledge about all the signals that are defined within.
So yeah.
All right.
Sorry, wrong name.
And the next next part, we're gonna talk.
I was planning to talk about.
How can you actually start to write these tests and what is the framework against that?
Sorry so.
Thinking about the sill architecture that we were just talking about when it comes to VCU, signal probes, signal injection and all that.
The integration test framework is how all of that gets used.
So think of that as like the test harness that kind of wraps together all these different types of inputs.
Into like a cohesive.
Environment to test within. So we have adaptive signal probes. This would be.
Any way you can kind of read and write posit signal or adaptive signals running on HPC. We have the local rig injector which is maybe more low level which is what you guys would be interested for the your auto loop application and then instrument cluster. This is prob.
More down the line or more relevant to Tony's work for the operator displays.
But these.
All these different pieces are meant to talk to one another, so you can kind of build out your.
Full sail system under test.
We have access to.
Objecting Ethernet. I guess that's your low level Ethernet there. So for injecting like in Arizona, communication for kind of our first ones, since we won't have like a low voltage power manager to send out the correct signals.
We'll be able to inject those signals via Ethernet, right?
Is the plan.
That's it'll be on the low level.
Signal OK.
Yeah, like your your guys's first use case is.
Sending out zone to zone Ethernet packets you can packets. Sorry.
And that's something you'll be able to do with this this test fixture.
Yeah, I think like oops, sorry.
Wasn't what I call it.
So delayed.
I bet.
Sorry, I lost my train of thought for the zone to zone communication. That is like that's like like table stakes or like, critical path for you guys to start testing auto loop because you need to essentially say.
Zone A is giving me this signal or the rear zone's giving me this signal.
How's all of it?
Consume it and how can I verify that?
But we'll also have signals from components that aren't developed yet, so this will be developing the component on the rear to take in.
A.
Physical input and then relay it.
But then there's also gonna be things that we need to fake.
To.
Fully test it because the components that are generating those aren't gonna be developed yet.
So you're saying?
Or like IMU or whatever is like a lower priority.
Yeah, manager, you need to be able to stop those signals as needed.
Yeah, thick those outputs so other things can consider.
Does this have?
I see canlin Ethernet.
Does this have physical signals then as well?
Current sensing, analog voltages, etcetera, etcetera.
I believe so.
That would fall under the.
Yes.
Highlighted that like 10 seconds ago.
So sorry if like what I've been showing hasn't been lining up, but yeah, that would fall under this.
Like the more the low level bus communications.
Yup, but I'll double check.
So for the sill testing here.
Talking about auto loan and we don't have the other subsystems built yet, so we're going to, I guess fake their inputs or outputs or whatever whatever auto needs to consume.
It's like vehicle speed or something like that. As we build up our system and then we have.
The code that would controllers and managers and whatever.
Would we?
Would our simulation grow to include those?
And we would never go back to just running the auto loop by itself or we would kind of do bolt where we kind of run subsystems on their own.
And mock those inputs and outputs and then also have a bigger test.
Or was that?
I think.
How I would say it is it's it's kind of up to you how you guys wanna test the system having auto Lube in isolation with like these other signals mocked out?
Makes sense in like early development. Let's say you guys are finished up with 930 and you wanna have an auto Lube on a different platform, a different business unit. You could still run those.
Stubbed tests in this case to get.
A. What do you call it?
Sense of like the the functionality of the functional requirements of AUTOLU but.
As you get more mature like you said, you're gonna want more realistic signal input here.
The cost or the like?
Trade. Trade off with that is, you know as you add in more complexity to what you're virtualizing or simulating, in this case you'll need stronger nodes, stronger test instances like stronger computers in this case to run that.
And at some point it might get to the point where.
Running all the containers virtualizing like the six different zones.
Sorry, four different zones running all the stuff.
Maybe not feasible to run, so there's kind of like a balance there in that case, but in ideal world you just run everything at at the same time.
OK, like I'm thinking of, OK, you've you've built up half the system now you wanna add in like hoist or something?
Are we gonna be spending a whole lot more time to bring up a virtualization or the whole rest of the system just to test the hoist?
Versus just running out in isolation and then kinda adding it in later because like if you're trying to develop some a new system, it's a lot of a lot more to bring in a whole bunch of stuff you don't care about.
Yeah, I think it also you.
Just popped in my head. Was like thinking about what's like the risk of the system. Like hoist is particularly impactful for like the functionality of.
Like loading and dropping off the OR. So that's pretty important.
So you wanna make sure it's able to effectively talk?
To what it needs to talk to.
So in my mind, that'll be a test, a case where you wanna bring up the rest of the system.
But for some.
Like ladder like you don't necessarily need it to have full knowledge of everything else. You kinda step those signals out.
It just depends. We go bowl place.
I know all these testing answers are so unsatisfying to me sometimes because it's it's. It depends, you know, but.
I just didn't know if there was, like, yeah, I definitely never go back to isolation, but just the amount of compute you're talking about makes that makes sense. So.
Just depends on case by case.
Yeah, I mean, that's something I can.
We could have, we could discuss with someone on the testing side, but that's how I see it.
I wonder how much time will will.
End up going back and adjusting all the other tests after we like complete the subsystem that makes sense.
So we start with auto Lube where we've stubbed out like the low voltage power stuff and once we.
Do the low voltage power stuff. Then we have to go back and update the auto loop test to include now no longer stub that, but to actually have a full pathway test.
Yeah. I mean, there's.
A couple ways of thinking about it.
You can either stub it in the autolo software component or like in that zone in that model.
Or you could like build out a skeleton framework of what?
Sorry, I forgot what the second manager you mentioned, but yeah, you build out a skeleton with low voltage to look like in the other zone or in the other like running in parallel to it.
And rather than having it like actually give out what the can message would be, you just kinda set it to like a true or false or have some script to define what those signals will be.
OK.
I'd be a fan probably of the latter set up. In this case 'cause it kinda gives you the architecture to start with, so it's at.
So it's at least going from output of A2 input.
Really care about the input, which I guess is probably how we should be doing these.
I don't know.
I go back and forth sometimes.
I just writing that down, yeah.
We should be able to provide that.
Develop the skeleton.
Interfaces.
Mm-hmm.
As we need it and then fill them out with all the.
Information.
That's not needed by other things.
When we do that actual development.
So as part of auto loops development, we'll have a skeleton for like low voltage power and other things.
Mm-hmm.
Basically, all those interfaces that we defined in the pallarian.
I know we're at noon and it's like lunchtime.
We have this room for the rest of the day.
So do you guys want to break for lunch now before we talk about the rest of integration testing or just go through it now?
Right over.
Right over.
OK.
Here.
Where's Jimmy John's?
Would you be fine with skipping our STV like our our stand?
Or I guess maybe take lunch.
Quick check in with stand up and then having this be our office hours like technically. Then go 'til 2.
Let's see that.
K.
Sounds good to me.
We'll break, get some lunch, check in with Lauren and Nick, and then come back after that.
You.
Did you have anything planned for office hours today?
I'd like to set up her.
I was going to review some of the questions we had yesterday, but I was preparing for this, so nothing specifically planned.
I think there's a point.
Break some steering meeting that I don't know.
That it'll actually happen or not.
I think it should have.
OK.
Good time then.
Get your golden ticket for this week.
I didn't get one for today, but that's fine.
You always just buy lunch.
Riley.
He'll grab 4 closets.
301.
Trying to eat passwords.
Update.
That's right after that.
After that.
Thanks, that's a problem.
Let's have a question on the.
Virtual SQ configuration.
You should.
Can use the chemo start script.
Is that where we define the executable name?
In Sanskrit, yeah, in that Sanskrit.
We have an example file.
Yeah, I'm trying to pull it up.
Should be 1 on your cluster.
Or on your repo.
So since are connected simult.
Aneously.
Nothing that you I.
But any other?
Fading if son alert.
The redundancy for Sun alert in the current system and if we need redundancy.
As the alarm that beeps at the operator when there's a fault.
If we need that redundancy, then.
I think that cab would be the central would be the most logical place for it.
Also use.
Must be monitor all the central.
Yeah, I think we'd have to go to central.
We have a portable cable going back.
Like we do for links and.
It's gotta.
It's.
Gonna. Yeah, Portland.
Yeah.
Any other GPA or?
Do you have a system?
But I think that would all be.
Very much depends.
I don't know.
Each one GPA.
Central should also to indicate that alive.
You're saying like a like the ignition signal.
Reset.
Or you're saying the out?
And GPA like I think it's like team move.
I like team move.
Yeah.
And that's connected to every quill.
Cool.
Yeah, that makes sense to me.
So GAIL.
I was like, oh, nice.
I'm doing unable to say.
Later I sort of indicator. I can, yeah.
Yeah.
I dunno what?
We'll have for like status LEDs or anything that would be useful though, yeah.
Not that I'll ask a question.
So Nathan, to your question, do you define the executables for?
Do you try to activate? No.
So the start script is what actually, you know gets the container going.
But you will need to deploy what is gonna get running on it after it's. So like you active you start up the container you're running the VM, then you need to deploy whatever's gonna go onto that hardware.
Sorry, OK, ECU absolutely that. And then that deploys like that moth orchestrate that I was talking about.
OK. That is what puts your executables onto the VECU.
And those are defined in your model build.
Ers like I'll exe, executables, library, whatever.
OK does that.
Answer your question.
Yeah.
OK, sorry I got distracted.
Let me share where we where we left off.
OK.
No, there was only two seconds left.
Time we saw left off talking about.
Sill, how we can talk get a signal probe in loop and then now we're actually gonna look at putting it all together and executing some integration level tests.
Umm.
And that is gonna be leveraged to what we call this integration test framework test framework that we see here.
Escort.
You can think of this test framework as like the core.
The core object or the core test object that wraps all of these together.
So you can kind of test everything concurrently, monitor, just monitor the information you need so on and so forth.
So lay we're gonna step through this talk about like what that integration test framework looks like. What kind of test fixtures you have available right now and we can talk about any gaps that you you may have?
Remember.
And then we'll talk about actually writing and running the test.
With looking at one of the example tests we have in in your repo.
Any questions before we move forward?
This is gonna include.
Just gonna include injections, I take it.
As part of this.
So kinda wanna probes briefly but.
Yeah, the injection part is part of this like local rate action.
Yeah. So the local I, I guess we didn't exactly cover this last time, but the local rig injector is essentially how you will send in canned traffic for your use case and how that gets monitored on on.
Ethernet and it's in from the back end.
It's essentially just like a CLI command you run, so you kinda define what the VM host is.
What the rig is?
What board do you wanna inject the signal to?
So on and so forth and that's the way you can kinda tap a specific can message into your.
Into your your application virtualized application and this is like the manual way of doing it, but you can sense the CLI. We could very easily script out a set of commands to send in and receive inputs that that might become a bit more clear when we look at.
Tests, but any questions?
Off the bat.
For basically setting a command line interface for each message you want to send, sending a command line prompt.
To inject a signal, yeah.
Is that a question or?
It is curious to see what it looks like.
So in terms of like what?
The what the?
Like sorry.
The command looks like.
Yeah.
Yeah.
So.
I guess for each application you or you can define like a rig injector application.
Or sorry, a client and then this will allow you to kind of establish what rig and board you can be sending it to and then you can use the inject can.
CLI to actually give the message in and you just have to specify the bus, the message ID and like what's going in there.
So this is assuming, I guess you're already assess.
Actually.
Interesting.
OK.
So this first part this CLI.
This is like an interactive CLI you can use to go into a given rig.
Mm-hmm. So this actually gets us into the VE CU board on my rig.
At this port or at this IP import.
So once you're inside this interactive CLI, you can run this injectcan command.
Why?
So some of the bus, the ID and the the data itself and it'll actually send a message to that to that board value.
And then alternatively or or looking at the other way, you can also probe that probe a given message so.
So it's the ID and you can probe whatever data and stream data from that bus.
Yeah. And I guess the same commands also exist for them as well.
Does that make sense?
I guess, yeah. What's that?
Yeah. Anything unclear? No.
My my question is coming from.
Like, how does this fit in our automated test case?
Process.
In your automated test process.
So how that would work in your automated test process for how to understand it, you essentially write a Python script, a pythest script, and this will, you know, be assessing some test case.
So if we stick to the, what is the example you gave earlier?
Like pulling in engine speed or something like that or you wanna tap into that you would create a test script that would essentially have a few different subprocesses to essentially.
Create that interactive CLI.
Enter in the injection command and then a separate sub process to do the same thing, but monitor track the output of that injection process.
Should be that probe creating that probe signal that we went through earlier, right?
Probes. Yeah, it would.
It would leverage that so the engine speed or whatever. I think that was what we talked about earlier.
Sure, that would be the signal name that we're probing against. And then?
That's gonna be traveling on some some bus that we could tap into or talk to, and then we can inject signals or read signals in there.
OK.
I mean, let's like walk through maybe what the framework and the examples are and that might clear up some of your confusion or seemingly skepticism.
OK.
Sorry, just trying to get windows all in order.
So this test framework like I mentioned is essentially a way to wrap all those different classes that we looked at. We looked at earlier in terms of adaptive signal probing, local rig ejection and then instrument cluster reading.
And this is built off of this framework. Test scripture from the Pyritest library.
And this is an example of like.
Defining a signal probe client to actually to actually read in some data.
For some field and this is kind of an example of what it looks like in in the Pi test framework.
Does did my field come from this?
Just a lack of my understanding of the adaptive.
Processor like how?
Do we you think you can think of my field as like the signal value for the signal name in this case?
So we can think of it as like engine speed.
Where it is set like. How does that actually tie into our pie arch implementation?
You define a signal in π arch.
It'll be named something.
Say that's the signal name, yeah.
Like the the port and right.
I think so. Yeah. OK.
Maybe from 100% a prior to signal names and you'll tie it to the signal name here.
Yeah, we define.
That be the system signals.
Notes.
Yeah, I don't know.
Just.
Port name is that system signal name.
I would imagine it's. I have no idea.
What is that?
Field.
Lot of different names and arch different layers.
Yeah, I don't know. I have to.
Get that answer for you.
If we don't define actual names.
A system signals don't have no way to put a name in as the actual port.
Required port provided port.
I'm guessing that's where it coming from.
So you're saying this patches too.
The actual port on a software component board.
Just the general.
Yeah.
General systems and.
Ports have to be like the port names have to be unique.
Residence.
Yeah. So trying to figure out where that name comes from, but I'll.
Let you know, OK.
'Cause I plan on having a lot of RP.
Switch.
I'm having a lot of port names being the same name.
Between different components.
The same thing.
Is the same thing.
Yes, please.
This is the same thing. Everyone's gonna be reading in the key switch signal, essentially.
People speak.
You keep alive Engine, just powertrain running except etcetera.
So I'd like all those.
Port names to be the same between.
Software components.
OK.
And I'd like to use the same interface ideally, but I'm about to go see if I'm doing that 'cause that's something I haven't tested yet.
I I wonder if it's also different 'cause is this with adaptive instead of classic?
Cause.
Yeah, I don't know what.
Know if there's a difference.
If it's our local.
Attach so I think this is only for adaptive 'cause we're looking at the adaptive signal probe in this case, OK.
From what I can tell, looking through the code base is you define like a given interface, so it will get door command.
That interface will have.
Like a service interface package and then the service interface to find event.
This event is essentially this. This interface defined event is essentially.
Connecting your door state to the interface and then how it gets distributed downstream, there's a name in that defined event, and that's what this event comes from, OK?
So I will just share this. What I'm looking at right now.
In.
So we look at they get this is only for adaptive. We look at the service interfaces we defined.
We have this door command interface and here we have this service interface package that.
We call it has a subclass or method called defined event and that name that we're looking at before it comes from here.
So that event I guess.
Maybe this applies?
Maybe more for PLM, but this would be defined empire.
I'm going to be a ******* here and I'm going to ask the question of who is the.
We talk about the capability of providing multiple instances of the same software component.
I don't know if we would use that yet.
It's definitely been put on the table for things like break controller.
The rear in the front but.
Does this still work if we have multiple instances of the break controller?
Software component running. They're gonna have the same exact definition with the same event names.
Stuff you know.
Patrons here.
If we're just relying directly on this defined event to have a unique name, what happens if we have multiple instances of the same software component running on different EC US?
How does it know which one?
We're interested in looking at or, yeah.
I mean if it has the same name, there is no great way to differentiate that.
So.
So.
The way you if if they have to have the same name because they have to have the same software component, I think like.
It would stem from where you're defining your pro.
So where are you looking in this case?
Umm, so where is that where we define where we're looking?
That would be defined in your test framework.
K.
So this probe that we're.
Defining is only for specific ECU.
Yeah, I because we were looking at the test signal probe.
You define it for specific ECU. No you don't.
No.
It's just a little system.
So is there?
Sure. I mean, if you're gonna have the same exact software component running on the front and the rear.
Without having.
But.
It'll definitely have the same interface variable.
So I guess this is adaptive reading a probe earlier we saw a classic where we were just reading the interface variable, right?
We'll run same issue both ways, right?
That's, I guess, another.
Linked up the issue I was bringing up.
Here.
I guess the answer is just have one called front and one called rear.
You do grand.
Meaningful.
OK, sure. But even the ports are named the same.
You'd have to have some sort of identifier of.
Coming from.
Yeah.
Which instance?
It's coming from.
Let's take.
Moving to the next part we look at.
Like how we actually run these tests.
You run them using the SPASL command, but each of them will have to have some necessary CLI flags.
So I don't, Joe. I think we like try this out or see like what it stems out to be, but.
If you have the same exact controller running on two different zones, same names, this could be a way you can.
Purposefully look at one place. OK, so you know that in this case, we're looking at.
Rear zone.
That's the.
My event the the breaking event that we're looking at.
But yeah, I I'd say we have to play around and see what happens, OK?
And this this applies like creating this CLI client applies for both.
The adaptive signal probe, which has these available fields in terms of what signals we can look at.
And then the rig injector, which is the.
Like firmware style in this case.
So yeah.
OK.
And looking at monitoring.
Like monitoring that data like we have this my event, this amorphous event that we defined somewhere that means something.
How do we actually track that we use this thing called collect stream?
So essentially that monitors a given interface for this events.
And you define like where you're looking based on like the Clr arguments for your basal test.
And this essentially just waits some period of time or period. A number of entries.
And then collects all the data that it gets between those entries.
You can also run multiple actions at the same time by using the like run all command.
This is the way you can let's say.
Put in a set of actions that you want to do so injector can have received the data in this case.
Or inject can send some data then receive it.
And this is where you can kind of monitor what you're injecting or adding and part of your sill test.
Questions.
OK.
OK.
So then looking at the available fixtures that we were just talking about.
Like I mentioned before, the CLI flags help you like.
Kind of like more narrowly scope. What? You're gonna be probing against or or checking or testing?
And then using the framework and there. So it's it's it's downstream methods you can say. So I wanna look at an adaptive client, look at a local rig and so on and so forth.
There are these things you can pass in to each one of your integration tests called markers.
So rather than having to run.
Each test by directory or by by name.
You can just run it by a marker instead. So if you have an engine test that live in multiple software components or in multiple zones or something like that, you can just do right at engine as your marker and then test using that.
Add those workers to those tests.
Sorry.
How do you add those markers to the test?
You would do so.
You have a test name.
It'd be like.
Engine test and then the marker would be encapsulated in the file name of the test, so it'd be like.
Would be so like engine, under score, diesel test would be that would be the marker. I think if you wanted to run diesel.
It says it here, so note that this name must end in a test suffix unmarked test run regardless, so.
You do as part of the test you've decorated with this ad.
High test dot Mark dot name and that will have to have some sort of under score. Test at the end of the name.
Third example, but don't look like.
You copilot it right now.
I'm searching Cortana's repo right now for exam.
See.
Can you stop?
So that we could have.
Was for free.
Software installed, support update.
For yourself.
That those ports are gonna be named the same.
Even if we wanted to, because it's a bad idea to.
Reuse the exact same chocolate so.
We have to create 2 separate oops. Let's see.
It's it's.
So I guess this is an example of like a marked test.
Where we have the marker up top, we'll be like adaptive smoke test here for it looks like speed to display test that we have for.
Vehicle S.
So this is how the markers defined.
They add smoke test.
New tag multiple.
Yes. So you can see there's multiple.
Back here, what do?
You mean you're saying multiple markers on the same test?
Yes.
I don't see why that wouldn't be possible.
But it kinda depends how the decorator gets read in this case.
OK.
Easy way to run kind of our configuration, no tests.
Only tests were all my electric test battery, test engine tests, et cetera.
Will.
Yeah you can.
You can apply multiple markers you.
You just like, do a list of them. Oh.
Oh.
It would essentially just be like.
Why didn't I buy the code mode?
Oh, there it is.
It would just be like at adaptive smoke test at engine test at this test. At that test in like subsequent lines.
So.
It would look like this so.
When was the first time I looked at Stack Overflow?
In many months, but.
Instead.
Stack overflow. That is what.
You mean if?
You look at their user base, it went up and then ChatGPT came in and then.
To be the life. There you go.
So that's how you define multiple markers. Cool.
Cool. Like right here.
I mean it is Stack Overflow.
So actually need to verify that's the case.
Seems like it makes sense.
Umm.
OK, that was what I had to talk about on test fixtures.
Why are we so let's go to writing and running tests.
So if we think about what it takes to run a test, we use π test, which is just like framework. That makes it pretty extensible and easy to.
Write and run these these integration tests that we've been talking about.
Typically or how we recommend setting up your test suite is we follow like this directory structure where your directory name this would be.
Or would it be in your repo?
It would be like firmware slash Cortana slash applications that would be this top level directory and then in each application you would have or. Sorry.
In in this director, you'd have a build file that defines how these tests will get build.
You'll have a runner, which essentially is what executes the syll test and a comp test, which is how you define all these fixtures that we were just talking about, like where we're gonna be injecting signals, how they're gonna get consumed when we're gonna be collecting so on and.
So forth.
And then a pie test configuration file.
Inside of this kind of application directory or sorry, this firmware directory, you'll have a test folder which essentially will just be how you would assess some of your tests.
OK.
Yeah. So I mentioned contest is just essentially a way to define.
The fixtures you're gonna be using.
At this location vehicle as that test integration test that has.
A set of comps tests that you can take a look at right now.
Or a set of fixtures. You can take a look at right now.
I can pull that up if you like.
If not, we can talk about the runner.
So the runner is essentially how we run the test. Is essentially just looking at.
The directory where you have the tests located in and just running through that list, or all of those. Assuming all of these tests take the same.
Parags you will have.
Essentially.
A bit of argue pass in the test will get run and then you'll consume the success or not. Any questions on that.
Yeah. So this would be the test directory.
This is how we would collect all the arguments you'd pass into your CLI.
They'll get passed to each one of your tests.
And then.
You don't get all trues, you get a failure.
And this is a very simple test runner in this case. But just to give you guys a sense of the process.
Yeah. So.
In terms of actually running the tests, this is like where we go back to what we were talking about, the ECU's, you know, you run MOG BCU for, let's say whatever rig you wanna work with. I think the rig in your repo right now is.
Good Sam Cabsun was a target.
What's the rig name?
Just trying to pull it up right now.
Oh, it's just called rig.
So the rig in your in your repo is called rig, but it'll be mod orchestrate rig rig dot YAML, deploy and start that or sorry start that will actually get the the ECU's running. So once they're running we actually have to deploy the software to those.
Virtualized instances, so this is where you deploy your specific app or your specific whatever is defined in that system composition file that I was talking about earlier.
Whatever you wanna run there.
And then you would run basal test wherever your tests are located and then put in your specific arguments.
And these arguments are like test configurations.
Vehicle configurations.
The type or anything like that?
Is that path to test suite looking for a file or is that a folder? What is that?
It's looking for.
This folder.
OK.
So it's looking for this directory name wherever your tests are located. It's gonna look at the build the runner, and then whatever tests are within.
So I think I misspoke earlier.
This doesn't explicitly have to live in firmer flat Cortana slash firmer slash slash application.
It could live anywhere. In this case K.
How do you?
Is something more needed to decide is how we communicate all these tests?
These directories.
One main directory then divide.
It up by some system result.
Are we going to run?
Yeah.
For his own test.
I guess we could add markers in there.
I mean, you could do.
That.
I think like what we do on like some of our automotive applications is like what Eric was saying is like a para method like what's the area?
What do we actually need to actually test?
One one of the tests that we need to test those areas you know.
And I'm missing a full sweep. Would look like just execute so one executes on 2, executes on three, executes on four, and then execute CP.
Hmm.
Yeah, I mean you would have probably just have where is it like one of these dedicated to each one of the zones that you want to test, execute those arguments, yeah.
Let's see an example in core stack to have.
Chevy dealer.
Yeah. I mean the example that's in your repository helpful and just kind of showing you.
The directory structure you guys are looking more for like a more complicated test structure. What's it gonna look like?
I'm just more of a hands on learner.
So I I learn a lot by doing so I I understand what you're putting down, but I'll probably have a a moment when I start writing these.
Sure. I guess like what's?
I know you said hands on, but like, what's the gap?
Maybe we can talk about it.
Edge nothing really is just I'm understanding, just I'm probably gonna start poking with questions once we start writing.
Just wanna point that out.
Don't.
Wanna some blind side of that?
I.
Expect questions all right.
Where does the eye test stuff live in Arko?
Where's pie test live?
Where it is all the all these still tests.
Like the examples, yeah.
Let's say you're very good.
Yeah, I'll show you in a second.
The V OS folder.
It's got this directory.
Uppal OS flash test slash integration tests.
Integration tests.
Test.
Forbidden land.
I would say forbidden.
You guys are allowed to look in there.
I mean, actually.
Change you. We can change it.
We just can't push it.
I mean, you can't. You can't.
We can push it just.
You'll just get. You can push and merge.
March it.
It'll, yeah.
Get overwritten. Yeah, that's true.
Try to sneak things in and then.
Try.
But yeah, this is an example of like the comps tests that I was just talking about.
And this is like how you define like the fixtures you wanna actually bring in so.
A lot of the examples or args that we're putting into this are like specific to what?
What's the rig?
What's the board?
So on and so forth.
Typically I guess when you look, you're running these tests. You wanna test them in CI, so you have some commit or some a specific thing you wanna.
Test against for like your build.
And you can say I wanna test on this.
This IP so on and so forth.
The support. Yeah, this is like kinda how you build out these fixtures, build out these args.
The next I wanted to look at an example test.
And just talk and talk through it.
So here we have an example.
Signal protest it's essentially.
Playing the game of Marco Polo, where we have Marco.
Marco trying to say hello.
But.
Rather than just saying hello and goodbye, it's essentially Marco's gonna pass a set of ints and polo's gonna square that that set of Ints and send it back.
So.
This just kinda walks you through the structure of setting up an adaptive signal protest.
This kind of mirrors what we were doing in pie arch or in the unit test for like SCU Home tutorial. Kind of initialize the system, essentially reset all the internal states of unknown values.
We're starting from a consistent place.
And then we actually analyze how the events are going to propagate.
So here we can see the marker.
It's called adaptive signal protests.
We define what the method is and then here is the input values that we want to send.
Out collect. I guess from Marco.
So here the oh, sorry from polo. Marco is gonna collect this data or essentially start a collection stream to receive.
Along this interface for Marco and collect that Marco event.
And then for every value in in this polo event values, we're just gonna loop through sending that, sending that value over.
So here's that pro client we were just talking about it sends.
This value 10 over the polo interface.
We wait until Marco, the Marco interface, or sorry collection collects it. Once we get that length of one, we essentially have it consume.
Once again.
And.
Sorry, we have it collected. And then next we essentially.
Read the response back from Marco to Polo.
That flow makes sense.
Yeah, I think so.
Is he gonna sit there and wait till?
Polo is done.
'Cause you're sending and then.
Waiting for the entry and then reading.
When you say wait like like the one loop iteration's gonna wait until.
Like, yeah, all the receipts back.
Is.
That what you're saying?
Yes.
Yeah, that's that's the topic.
And then as part of this, like Marko monitoring that, I was just talking about like we're collecting those, that data that we're getting back.
So.
We just wanna make sure that we're getting like the square values that we expect and so on for normal.
Like this. Looks like we've had.
We have an event to say that we've read.
Like normally, how long do we need to wait for propagation?
So we set an impulse on one side and we want to read it on the other.
Here we're setting the input. We're waiting for an event to say yes.
We received something and then we're checking.
Do you normally need to have that wait for propagation or how does that?
I'm not sure what the question is.
So in this flow, here we have.
See this here.
So we're sending the event polo event, right?
We're sending a value with that polo event, and then the next place enter in this entries.
We're monitoring the Marco event and we're waiting for that to receive it.
Before we continue with our comparison and most of the stuff that I can think of, we're not gonna have an event defined saying that we received something.
I got on the firmware side of things.
So is there weights that we need to have to make sure that things propagate all the way down before we check the other end?
Before we go on that, when you say you're not gonna be having an event or something to consume on the firmer side, what do you mean?
So this that that Marco event is.
Generated.
Will be generated in the pie arch like the software component definition.
You all right?
That's not gonna exist. Like, we're not gonna have.
I guess.
It's not quite a one to one comparison, so I'm trying to think of what the equivalent on the firmware side would be, and I don't know if there is an equivalent on the firmware side where we would say yes, we've like the event has propagated all the way.
Through.
Click back.
Yeah.
Like, do you get the? Do you get the ask?
I do get the ask.
I mean like.
I'm not as familiar with the firmware side, so I'm trying to think.
How would work?
Yeah, but in my mind you send out a signal and you wanna get some response.
How are we gonna be measuring that response?
Is is the key question.
Yeah.
And what what is that interface or is that probe gonna be in this case?
That's the question, right?
No, the question is.
How do we do? We need to have weights in here to make sure that data is propagating.
Through the components.
Like so, the autoloop example, we have a switch on the rear zone, right?
So we would simulate that switch changing state.
That's our input.
But then that state has to go.
Into the rear zone.
It's got to do its logic.
It's got to make it on to the Ethernet bus.
It's got to read.
On the front zone and then the front zone has to turn on the output, right?
If we're probing that output and we want to make sure that the output does what it should.
Based off of the input switch.
Is that gonna be automatic? And as soon as we set the input, we should expect to see the output.
Where is their propagation time in here?
'Cause it looks like you guys are accounting for that propagation time with that wait for.
The Marco event.
Yeah, I think.
I mean, I'm brainstorming here, but I think that would what that would look like is like rather than creating like an adaptive signal probe client, we would do like a rig injector client, yeah.
That would be streaming a given set of can frames or whatever data you want to be streaming for sure on the firmware side, and so on the firmware side you would send out if you go back to the audio example.
Or you be what monitoring pressure switch in this case?
Or.
Could be inject injecting pressures.
The pressure.
Job put. Yeah. We be injecting pressures into the state machine or or to the app and then the.
Sorry, just going back the.
Monitor Marko event in this case would just be like a monitor. Auto loop can message and that would be pressure in this case and you would wait until you get.
You'd wait till you get some value that makes sense to you in terms of, like when the full depressed switch on and off.
So what that would be is you can modify that by like number of entries you want to get.
Make sure we get at least 10 entries or whatever that is.
Check if the pressure fell below some threshold or whatever your test is trying to do.
And then that's how.
You can move forward through this test, but we don't need to worry about propagation time. As soon as we set an input that should immediately.
I mean, I don't think.
I can't say it's gonna be immediately propagated, but like the idea with this monitoring event is that it's.
Like are you trying to test specifically the propagation time like you wanna make sure that it's happening within a given?
He just wants.
To know what time.
Period. What propagation time is not necessarily just do I need to account for the most the stuff that I owe?
Know you should not need to manually account for it, that should handle.
Well.
Says that we're gonna write.
It's just gonna be like something like this where we inject, we send the event and then we expect to see an output like. There's nothing in here to wait.
On most of stuff, we'll just then be reading send event, read field, right?
OK.
Do we need to have anything in between?
I guess and and what if we do want to wait if we want to send it and we want to figure out how long it takes for that output to come on.
Is that a capability?
Yeah, I mean, you can fill that in.
I mean I could check if it's built into like the frame test features that I was talking about, or like, I don't think there's anything stopping you from like putting in like a timer and assessing it from that perspective. OK or putting in like a wait rather than.
Assert here, just like putting a wait saying.
Milliseconds or microseconds or whatever, not microseconds. You know what I mean?
Yeah. Yeah. Hey.
OK.
Yeah, yeah, is still testing meant for more logical A to B data movement or is it meant to account for that time delay?
Through specific networks.
I think it's mainly meant for the A to B. OK thinking that.
And you can spend billions more of timing requirements.
Definitely, yeah.
But it's it's simulating the actual tests.
So if I.
Set like.
If there's a debounce on the signal right and I send it and then read, exactly like if there's gotta be a three second wait in the simulated.
Time. Yeah. There's gotta be a real.
Time aspect to it, for it to actually propagate through and for us to see.
Yes.
The output accident.
Is it?
Is it running real time or do you do?
Like.
A simulated step time.
It can run real time.
In theory, if you have enough resources.
Not sure.
What the DT we define for? I think it's whatever like the V Miss Clock time is in.
This case, it's like, yeah, the debounce. If you have a 300 millisecond, this has to be true.
How do you get through that 300 milliseconds?
Yeah. I guess in the case of like these V Miss, they are gonna have some sort of like wall.
No, not wall.
Time would be real time.
They'll have some sort of like SIM time that would be keeping track of. That would be the clock in the VM.
Yeah. So you would go against that?
Can we measure the the timing that it takes to go from an input?
To an output you would have to put in.
I have to check if that files in but like you would have to put that in to here.
Umm.
I test.
Yeah, that's.
Yes, Cortana.
Should they gonna be representative?
I gotta hop off too.
Same as well.
Bye Tess.
That's built in ways to measure test timing, but I don't know if that's gonna measure the timing between each one of these.
That is which I which is what I think you want in this case, right?
Not really.
We just wanna see if we set a bunch of inputs. How long does it take for the outputs to go?
Hey, we saw you.
Oh, then that would be here.
That would just you just essentially do like timer start and yeah.
Yeah. And then we'd have to keep on reading.
Read field.
Right, we'd have to keep on iterating over read field until we see the value that we expect to see.
Yeah, you can do some wild condition there. Yeah. OK.
You want me in there, Joe plus.
Wouldn't it hurt?
OK.
Thanks to.
Adjourn for.
An hour. All right. Yeah, sure.
Hello.
Our stairs today we have Alex here.
You should see it in Appalachia.
Skip.
Huh.
You want to come soon.
Just see what I'm talking about.
Oh yeah, for the you wanna have me join?
On zero basis.
Yeah, I'll join.
We can initiate unit that's fine.
The what?
The gold standard on a circle on the lab.

Joseph Boyer stopped transcription