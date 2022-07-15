# EELSTM: Time Series Prediction on Electron Energy Loss Spectra

## Table of Contents

- [Program Detail](#program-detail)
- [Requirements](#requirements)
- [Installation](#installation)
  * [Download Git Repository](#download-git-Repository)
  * [Create environment](#create-environment)
  * [Install required packages](#install-required-packages)
  * [Relaunch](#relaunch)
- [Web Interface](#web-interface)
- [Data](#data)
- [Group Members](#group-members)
- [Contact Information](#contact-information)
- [Acknowledgments](#acknowledgments)
- [Usage License](#usage-license)

## Program Detail

This is the repository of DIRECT Capstone program, supported by the Data Intensive Research Enabling Clean Technology (DIRECT) National Science Foundation (NSF) National Research Traineeship (DGE-1633216), the State of Washington through the University of Washington (UW) Clean Energy Institute and the UW eScience Institute. 

## Requirements

You need to either download our GUI project or jupyter notebook under `working notebook` path to use our production. Please follow the installation steps.

## Installation

For user familiar with the command line:

### Download Git Repository

1. `cd <replace with location of project folder>`
2. `git clone https://github.com/Yjin232/PNNL_LSTM_GROUP.git`
3. `cd GUI`

### Create environment

For Mac users:
1. `python3 -m venv env`
2. `source env/bin/activate`

For Windows users:
1. `virtualenv env`
2. `\path\to\env\Scripts\activate`

For Pycharm users:
1. Open the project under the `GUI` root
2. Click the `install the requirements.txt` button

### Install required packages
Make sure your device could run the `PyTroch` and `Keras`
1. `cd GUI`
2. `pip install -r requirements.txt`

### Relaunch

To reactivate environment:
1. `source env/bin/activate` #if have mac
2. `\path\to\env\Scripts\activate` #if have windows
3. `cd to GUI folder`
4. `python app.py`

- For ease of use a demo video has been included in the repository under `GUI Demo`

## Web Interface

Our GUI is based on Flask version == 2.0.1 and we integrated two main functions in it, one is few-shot machine learing for image segmentation and feature classification in transmission electron microscopy (TEM), see detail in `pychip_gui` Repository Link: https://github.com/pnnl/pychip_gui.

Another is for LSTM time series prediction for STEM spectrum, more details are given in the associated manuscript.
![image](https://github.com/Yjin232/PNNL_LSTM_GROUP/blob/main/sample.png)

* Data Import: The GUI only accpet STEM specturm data in .dm4 format, the data file should contain a singal part and raw data on different time series.

* Specturm Visualization & Model Choose: The GUI would visualize the spectrum in time series and could control by a slider bar, try drag the silder bar to see the spectrum change in different time step. In this page, you also need to choose the dwell time for your STEM specturm data, and then click the submit button.

* Prediction Display: The GUI provides the final prediction graph which includes the prediction, real one and the input sequence, also the Mean Sqaure Error(MSE) for the prediction evaluation. Try downloading the chart by clicking the `download` button.

* Prediction History: The GUI provides a learing history page to keep the track of the results of prediction, use `detail` button to download the results and `delete` button to delete the results.

## Data

- Our STEM Spectrum data is under the `Data` folder, all of the specturms were under the condition: 0.1 eV, Point Scan 0.8 seconds with 0.08 - 0.8s dwell time. 

## Group Members

- University of Washington DIRECT Capstone Program Students: Nicholas Lewis, Yicheng Jin, Xiuyu Tang
- Pacific Northwest National Laboratory: Steven Spurgeon, Sarah Akers, Christina Doty

## Contact Infomation

## Acknowledgments

## Usage License

Copyright 2022 Battelle Memorial Institute

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Disclaimer
======================
This material was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any of their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.


<p align='center'>PACIFIC NORTHWEST NATIONAL LABORATORY <br>
<i>operated by</i><br>
BATTELLE<br>
<i>for the</i><br>
UNITED STATES DEPARTMENT OF ENERGY<br>
<i>under Contract DE-AC05-76RL01830</i></p>
