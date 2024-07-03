from roadmaps.roadmap_node import RoadmapNode
import os


def create_basic_skills() -> RoadmapNode:
    job_description = RoadmapNode(name="What are Jobs", prompt="Explain Jobs on HPC systems, slurm, and sbatch scripts.", children=[])
    resources = RoadmapNode(name="HPC Resources", prompt="Explain types of resources that are commonly requested for jobs, including CPU, GPU, and memory. Explain the limited nature of HPC resources and how they are shared, and why it is therefore important to know the extent of resources to request for a job.", children=[])
    submitting_jobs = RoadmapNode(name="Submitting Jobs", prompt="Explain the process of submitting an sbatch script in detail, and also explain how srun works. Describe the differences between these two approaches of running jobs.", children=[])

    hpc = RoadmapNode(name="What is HPC?", prompt="Explain what a High Performance Computing cluster is and why it is important to researchers in all fields.", children=[])
    hpc_technical = RoadmapNode(name="HPC Technical Details", prompt="Explain what a High Performance Computing cluster is made up of, describing nodes and the components within nodes with specific examples.", children=[])
    accessing_hpc = RoadmapNode(name="Accessing HPC", prompt="Explain how to connect to servers (including HPC clusters), and in doing so explain the ssh command and how to use it.", children=[])
    jobs = RoadmapNode(name="Jobs", prompt="", children=[job_description, resources, submitting_jobs])
    servers_hpc = RoadmapNode(name="Servers/HPC", prompt="", children=[hpc, hpc_technical, accessing_hpc, jobs])

    github = RoadmapNode(name="Git, Github, Gitlab", prompt="Explain what Git is, and what Github and Gitlab are, and how they are useful for HPC due to making it easier to share code and applications.", children=[])
    install_git = RoadmapNode(name="Install Git Locally", prompt="Explain how to install Git on a local system. Then explain how this relates to Github, explaining how to connect local to remote and what the difference is between Git and Github.", children=[])
    clone_git = RoadmapNode(name="Clone Git Repository", prompt="Explain how to clone repositories from Github.", children=[])
    branches = RoadmapNode(name="Branches", prompt="Explain what Github branches are and how to work with them.", children=[])
    contributing = RoadmapNode(name="Git, Github, Gitlab", prompt="Explain Git commit, pull, push, pull requests, and merge conflicts, and how to apply these concepts when contributing code to a git repository.", children=[])
    git = RoadmapNode(name="Git", prompt="", children=[github, install_git, clone_git, branches, contributing])

    basic_environment = RoadmapNode(name="Basic Environment", prompt="Explain Linux and the command line to someone who has only used GUIs.", children=[])
    directories_navigation = RoadmapNode(name="Directories and Navigation", prompt="Explain directories and navigation in Linux, from the context of GUI folders and files.", children=[])
    files = RoadmapNode(name="Files", prompt="Explain how to display and edit files in the command line in Linux.", children=[])
    permissions = RoadmapNode(name="Permissions", prompt="Explain permissions in Linux.", children=[])
    wildcards = RoadmapNode(name="Wildcards", prompt="Explain wildcards in Linux.", children=[])
    aliases = RoadmapNode(name="Aliases/Env Vars", prompt="Explain Aliases and Environment Variables.", children=[])
    basic_linux_skills = RoadmapNode(name="Basic Linux Skills", prompt="", children=[basic_environment,
                                                                                     directories_navigation, files,
                                                                                     permissions, wildcards, aliases])

    root = RoadmapNode(name="Basic Skills", prompt="", children=[basic_linux_skills, git, servers_hpc])

    root_json = root.to_json()
    with open("roadmaps/basic_skills.json", "w") as outfile:
        outfile.write(root_json)

    return root


if __name__ == "__main__":
    create_basic_skills()
