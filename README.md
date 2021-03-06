# AES: A composition automatic scoring system with word recommendation and data visualization

## Introduction
This is the Flask and Vue implementation of our paper "[Design and Implementation of an Automatic Compositions’ Scoring System for Chinese Learners](https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&dbname=CJFDLAST2021&filename=DZRU202021059&uniplatform=NZKPT&v=vwj5CCu_UCCZyvXrjDNMM2IN8OH4elnsDEkiKLFZ-lwMX3RXtB_ccqT_vpnM_4AI)"

## System 
![Customer homepage](https://s2.loli.net/2021/12/09/aYgxmM2uCIyzb5c.jpg)
![Submit essay](https://s2.loli.net/2021/12/09/J4vXY6ymEqGUuQA.jpg)
![Result of scoring](https://s2.loli.net/2021/12/09/sKNSAkqjaOrHeLx.jpg)
![History](https://s2.loli.net/2021/12/09/rWvtG6ABNyjOeh7.jpg)

## Startup project

### Requirement
```bash
#install npm and vue_cli, then
cd client 
npm install

#install python, create an vitual environment, then
cd server
pip install -r requirements.txt
```

### Database
```bash
#install mysql, then
mysql
>CREATE DATABASE `aesdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

#init database
python manage.py db init
#migrate database
python manage.py db migrate
#upgrade database
python manage.py db upgrade
```

### Run
```bash
#run client
cd client
npm run dev
#run server
cd server
python run.py
```

## Citation
```
[1]张恒源,李大卫,安佳宁,刘洋.面向汉语学习者的作文自动评分系统设计与实现[J].电子技术与软件工程,2020(21):127-130.
```
