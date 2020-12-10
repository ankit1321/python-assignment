# python-assignment

    fork this repo and start your work
    
## Getting Started

#### Pre-requisite : Python 3.7.1

    $ pip install --upgrade pip
    
    $ pip install -r requirements.txt
    
    $ python main.py [--dataset "dataset_folder_name"]
    
In last command operation in square braces are optional. All images in dataset folder will be pretrained by machine.

## Docker

### Build dockercontainer

    $ docker build -t accountname/projectname .
    
By running above command you can build docker image (Dot in above line is compulsory. It represents current directory).

### Direct run docker image

    $ docker run ankit1321/bipolar
    
### Pull docker image to local computer

    $ docker pull ankit1321/bipolar
    
Currently this image is working on some system if dockerimage detects camera from system.  
When camera is not detected it is showing error of "no available video device".  

## I am currently working on it. Fully working docker will be Updated soon.
