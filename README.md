## Домашний проект по курсу "Асинхронная архитектура"
3-й поток

Ссылка на общие требования к домашнему заданию: https://lms.tough-dev.school/materials/1cf623e0c65f4123bf6a809b4cd89e12/
## ДЗ 1
### Задание
* Разобрать каждое требование на составляющие (актор, команда, событие, query). Определить, как все бизнес цепочки будут выглядеть и на какие шаги они будут разбиваться.
* Построить модель данных для системы и модель доменов. Рисовать можно в любом удобном инструменте (включая обычную бумагу), главное, чтобы это было не только у вас в голове, но и где-то вовне. Благодаря этому вы сможете сфокусироваться на отдельной части системы, не думая о других. А также показать свое решение одногрупникам/коллегам.
* Определить, какие общие данные нужны для разных доменов и как связаны данные между разными доменами.
* Разобраться, какие сервисы, кроме тудушника, будут в нашей системе и какие между ними могут быть связи (как синхронные, так и асинхронные).
* Определить все бизнес события, необходимые для работы системы. Отобразить кто из сервисов является продьюсером, а кто консьюмером бизнес событий.
* Выписать все CUD события и какие данные нужны для этих событий, которые необходимы для работы системы. Отобразить кто из сервисов является продьюсером, а кто консьюмером CUD событий.

### Отчет о выполнении ДЗ 1
#### Состав
1. Диаграмма [event storming](#event-storming)
2. Диаграмма [data model](#data-model)
3. Диаграмма [ER с разделением на домены](#er-model)
4. Диаграмма [структурная](#structure-model)
5. Описание бизнес событий системы
6. Описание CUD событий системы
#### <a name="event-storming"></a> Event storming diagram
![Event storming](https://github.com/RBizonDota/CourseMicroservices/blob/DZ1/docs/diagrams/event-storming-v3.drawio.png)
#### <a name="data-model"></a> Data model diagram
![Data model](https://github.com/RBizonDota/CourseMicroservices/blob/DZ1/docs/diagrams/data-model-v1.drawio.png)
#### <a name="er-model"></a> ER diagram
![ER model](https://github.com/RBizonDota/CourseMicroservices/blob/DZ1/docs/diagrams/data-model-ER-domains-v2.drawio.png)
#### <a name="structure-model"></a> Структурная схема
![Structure model](https://github.com/RBizonDota/CourseMicroservices/blob/DZ1/docs/diagrams/structure-diagram-v2.drawio.png)
#### <a name="business-events"></a>  Описание бизнес событий системы
1. **Tasks.StatusChanged** 
    * Procucer: TaskTracker 
    * Consumers: Payment, Analytics
    * Создается при изменении статуса задачи (при ее завершении)
2. **Tasks.Reassigned**
    * Procucer: TaskTracker 
    * Consumers: Payment, Analytics
    * Создается при шаффле задач
3. **Payment.FeesPayed**
    * Procucer: TaskTracker 
    * Consumers: EmailNotifier
    * Создается при подсчете необходимой выплаты в конце дня
4. **EmailNotifier.Sent**
    * Producer: EmailNotifier
    * Consumer: Payment
    * Создается после отправки сообщения-заглушки проведения оплаты. Вызывает создание записи в аудите. Нужно для создания записи в аудите (чтобы сумма всей истории сходилась с текущим значением баланса)

#### <a name="business-events"></a>  Описание CUD событий системы
1. **Account.Created** 
    * Procucer: Account 
    * Consumers: TaskTracker, Payment, Analytics
    * Создается при добавлении новой записи пользователя. Синхронизирует связанные таблицы
2. **Tasks.Created**
    * Procucer: TaskTracker 
    * Consumers: Payment
    * Создается при добавлении новой записи задачи. Синхронизирует связанные таблицы
3. **Payment.Created**
    * Procucer: Payment
    * Consumers: Analytics
    * Создается при добавлении новой записи в аудит. Синхронизирует связанные таблицы