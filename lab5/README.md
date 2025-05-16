## Лабараторная работа №5
**Предмет: Программная инженерия**<br>
**Выполнил: Носов Александр Сергеевич, М80-114СВ-24**  <br><br>
1. Для данных, хранящихся в реляционной базе PotgreSQL реализуйте шаблон
сквозное чтение и сквозная запись (Пользователь/Клиент …);
2. В качестве кеша – используйте Redis
3. Замерьте производительность запросов на чтение данных с и без кеша с
использованием утилиты wrk https://github.com/wg/wrk изменяя количество
потоков из которых производятся запросы (1, 5, 10)
4. Актуализируйте модель архитектуры в Structurizr DSL
5. Ваши сервисы должны запускаться через docker-compose командой dockercompose up (создайте Docker файлы для каждого сервиса)

Рекомендации по C++
- Используйте фреймворк Poco https://docs.pocoproject.org/current/
- Пример по работе с Poco Web Servers и Redis
https://github.com/DVDemon/arch_lecture_examples/tree/main/hl_mai_lab_05

Рекомендации по Python:
- Используйте FastAPI для построения интерфейсов
- Простой пример применения redis
https://github.com/DVDemon/architecture_python/tree/main/07_redis

Тест производительности:

1 поток без Redis
```bash
Running 10s test @ http://localhost:8001/api/v1/user/get_all
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    60.56ms   59.07ms 487.26ms   94.51%
    Req/Sec    16.63      3.51    18.11     89.21%
  191 requests in 10.74s, 49.11KB read
Requests/sec:     16.49
Transfer/sec:      4.51KB
```

1 поток с Redis
```bash
Running 10s test @ http://localhost:8001/api/v1/user/get_all
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    44.75ms    4.89ms  55.17ms   77.81%
    Req/Sec    16.11      2.26    18.52     92.66%
  193 requests in 10.05s, 49.15KB read
Requests/sec:     17.28
Transfer/sec:      5.06KB
```

5 потоков без Redis
```bash
Running 10s test @ http://localhost:8001/api/v1/user/get_all
  5 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    62.41ms   10.48ms 129.55ms   67.12%
    Req/Sec    15.99      4.91    20.00     60.00%
  800 requests in 10.01s, 209.99KB read
Requests/sec:     79.90
Transfer/sec:     20.97KB
```

#### 🔄 5 потоков (с Redis)
```bash
Running 10s test @ http://localhost:8001/api/v1/user/get_all
  5 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    62.07ms   10.73ms  99.25ms   59.70%
    Req/Sec    16.06      4.89    20.00     60.80%
  804 requests in 10.02s, 211.04KB read
Requests/sec:     80.26
Transfer/sec:     21.07KB
```

#### 🔄 10 потоков (без Redis)
```bash
Running 10s test @ http://localhost:8001/api/v1/user/get_all
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    88.57ms   79.79ms 565.57ms   93.25%
    Req/Sec    14.28      5.27    20.00     52.82%
  1460 requests in 10.90s, 382.72KB read
Requests/sec:    133.90
Transfer/sec:     35.10KB
```

#### 🔄 10 потоков (с Redis)
```bash
Running 10s test @ http://localhost:8001/api/v1/user/get_all
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   104.17ms  131.97ms   1.18s    92.42%
    Req/Sec    14.25      5.31    20.00     53.35%
  1445 requests in 11.14s, 379.17KB read
Requests/sec:    129.75
Transfer/sec:     34.05KB
```
