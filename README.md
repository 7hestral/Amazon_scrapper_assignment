# Amazon_scrapper_assignment
## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [License](#license)

## Introduction
A traditional scrapper for downloading order details in html format.

## Prerequisites
This project is created using:
- Python >= 3.8
- Google Chrome 126.0.6478.127.
- Conda 24.5.0


## Installation
1. **Clone the repository**:

```
git clone https://github.com/7hestral/Amazon_scrapper_assignment.git
cd Amazon_scrapper_assignment
```

2. **Create virtual environment**
```
conda create -n venv python=3.8
conda activate venv
pip install requirements.txt
```

## Configuration
Before running the project, you need to create a `config.py` file with the following variables:
```Python
profile_path = "path_to_your_chrome_user_data_directory"
profile_name = "name_of_your_chrome_profile"
email = "your_amz_email@example.com"
password = "your_amz_secure_password"
```
Follow the instruction in [link](https://stackoverflow.com/questions/70825917/selenium-common-exceptions-webdriverexception-message-unknown-error-devtoolsa) for creating the profile path and profile name,

## Running the project
The project can be run using ```python main.py```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
