https://www.educba.com/lxd-vs-docker/
https://ubuntu.com/blog/lxd-vs-docker

# Docker vs LXD:

## Docker :

Application containers (such as Docker), also known as process containers, are containers that package and run a single process or a service per container. They run stateless types of workloads that are meant to be ephemeral. This means that these containers are temporary, and you can create, delete and replace containers easily as needed.

Docker is a containerisation platform, it can be installed on a machine (workstation or a server) and provides a variety of tools for developing and operating containers. One of those tools is containerd – a daemon-based runtime that manages the complete lifecycle of Docker containers, including overall running and monitoring of containers. Docker abstracts away storage, networking, and logging, making it easy for developers that don’t have much prior Linux knowledge. Docker was specifically designed for microservice architecture, providing a way to decompose and isolate individual processes, which can then be scaled independently from the rest of the application or system they are a part of.

## LXD:

System containers (as run by LXD) are similar to virtual or physical machines. They run a full operating system inside them, you can run any type of workload, and you manage them exactly as you would a virtual or a physical machine. System containers are usually long-lasting and you could host several applications within a single system container. If you’re curious, in What are Linux containers blog, we go a bit deeper into the history of system containers, how they led to LXC, and ultimately, LXD. 

LXD utilises LXC for running system containers. LXC is the technology allowing the segmentation of your system into independent containers, whereas LXD is a daemon running on top of it allowing you to manage and operate these instances in an easy and unified way. When it comes to storage, networking, and logging, LXD supports a variety of interfaces and features that the user can control and interact with. LXD is image-based and you can utilise it to run any kind of workload, including traditional systems you would otherwise run in physical or virtual machines. Overall, functionality-wise, LXD is similar to VMWare or KVM hypervisors, but is much lighter on resources and removes the usual virtualization overhead.

## Comparison between LXD and Docker

|             | LXD                                                                                                                                             | Docker                                                                                                                                                                                                                                                                   |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Integration | LXD can be integrated with fewer tools and technology, only with OpenNebula and Openstack.                                                      | Docker can be integrated with more tools and technology like Kubernetes, Jenkins, Ansible, and all available Public Cloud.                                                                                                                                               |
| Portability | LXD is less portable than Docker.                                                                                                               | Docker is more portable.                                                                                                                                                                                                                                                 |
| Popularity  | LXD is not much popular in comparison with Docker as LXD has 2.5k stars and only 604 forks on Github.                                           | Whereas Docker is an industry-leading container platform as Docker has 56.6k starts and 16.3k forks on Github.                                                                                                                                                           |
|             | LXD is being used by Deck-D, Stockopedia, GEMServers, and tutuf.                                                                                | Docker is being used by Spotify, Pinterest, Twitter, and even Google.                                                                                                                                                                                                    |
| Simplicity  |                                                                                                                                                 | The simplicity that Docker offers to developers is what made it so popular                                                                                                                                                                                               |
| Speed       | The performance difference between LXC and Docker is almost insignificant.                                                                      | The performance difference between LXC and Docker is almost insignificant.                                                                                                                                                                                               |
| Security    | It gives you security features, including Linux capability support, to help you keep control of your container environment and the hosted apps. | Docker’s approach of keeping the different application components in separate containers is a plus. But this strategy also has its own security downsides if you’re hosting complicated applications that may require the attention of an experienced security engineer. |
| Ease of Use | Both LXC and Docker are easy to use and provide documentation and guides to help you create and deploy containers.                              | Both LXC and Docker are easy to use and provide documentation and guides to help you create and deploy containers.                                                                                                                                                       |
| Scalability | LXC is less scalable compared to Docker.                                                                                                        | With Docker, you can break out the functionality of applications into individual containers.                                                                                                                                                                             |
| Operating System | LXD is linux based.                                                                                                        | Docker is runs natively on both windows and linux.



## Opinion:

In my opinion, I believe docker is the better fit for our needs. The ability to break out the functionality of an application into individual containers is most important for us, since we can seperate the database from the rest of the application and since our application is not that big in scale we do not about have to worry deeply about the maintenance of multiple containers and Docker offers the flexibilty of running on both windows and linux.


### Resources:
https://www.educba.com/lxd-vs-docker/
https://ubuntu.com/blog/lxd-vs-docker
https://www.youtube.com/watch?v=Q5J9N67z_SM&ab_channel=Scotti-BYTEEnterpriseConsultingServices

https://earthly.dev/blog/lxc-vs-docker/

