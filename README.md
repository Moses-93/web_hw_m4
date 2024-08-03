# web_hw_m4

1. Clone this repository

```bash
git clone https://github.com/Moses-93/web_hw_m4.git
```

2. Pull down the container 

```bash
docker pull moses93/my_server:0.0.1
```

3. Start the container

```bash
docker run -it -p 5000:5000 -v </your/path>:/web_hw_m4/front-ini
t/storage --name my_server moses93/my_server:0.0.1
```

