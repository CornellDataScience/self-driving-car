## Building and running docker
1. Download docker desktop: https://www.docker.com/products/docker-desktop
2. Build docker image
  - Run: "docker build --tag self-driving-car ."
3. Running the docker image
  - When QT works runDocker.sh script will setup enviorment/ permissions and run docker image
    - Run: "sh runDocker.sh"
  - For now comment out any display_frame refrences in main control loop
    - Then run: "sudo docker run self-driving-car python3 -m src config_file_name test_case_name"
    - For example: "sudo docker run self-driving-car python3 -m src hootl.yaml NoSIM"

*To edit the docker image, edit "dockerfile" 
*To edit the process of changing the enviorment and running the image, edit "runDocker.sh"