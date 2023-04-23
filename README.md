# Бот для просмотра расписанияя из уникума
Мы с моими одногрупниками заметили, что сайт с расписанием у нашего центра довольно неудобный и что-бы посмотреть свое расписание нужно долго искать нужную группу и обновлять страницу с расписанием для нее, потом искать нужный день и на все это уходит много времени, поэтому я вместе с нашим преподователем Владиславом решили создать данного телеграм бота.</br>
В проекте используются базы данных sql, aiogram 3, beautifulsoup 4.</br>
Наш бот может отправить вам информацию для указанной вами группу на сегодня, либо самое ближайшее с указанием даты. </br>
При указании группу наш бот автоматически проверит есть ли она в списке с сайта с расписанием, далее возьмет ссылку для укзанной группы с сайта и найдет расписание среди таблиц на этой странице.
