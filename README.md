## Wheellog_Graph ##
Программа Wheellog_Graph предназначена для анализа csv-логов Android-программы Wheellog (для моноколес)
Рисует графики скорости, мощности из csv-логов и позволяет их масштабировать колесиком мыши.



> [Wheellog](https://play.google.com/store/apps/details?id=com.cooper.wheellog&hl=ru) - приложение для Android, которая работает с моноколесами Inmotion, Kingsong, Gotway, Ninebot и позволяет видеть метрики с вашего моноколеса, записывать логи, и менять некоторые настройки.

Скриншоты Android-приложения Wheellog:    
![Скриншот Android-программы Wheellog 1й экран](https://github.com/Storvild/resources/blob/master/img/wheellog_graph/wheellog01.jpeg?raw=true)![Скриншот Android-программы Wheellog 2й экран](https://github.com/Storvild/resources/blob/master/img/wheellog_graph/wheellog02.jpeg?raw=true)![Скриншот Android-программы Wheellog 3й экран](https://github.com/Storvild/resources/blob/master/img/wheellog_graph/wheellog03.jpeg?raw=true)

## Wheellog_Graph ##    
Системные требования:   
    Python3    
    Библиотеки: tkinter и matplotlib

Скриншоты программы Wheellog_Graph:
![Скриншот программы Wheellog_Graph](https://github.com/Storvild/resources/blob/master/img/wheellog_graph/001.jpg?raw=true)
![Скриншот программы Wheellog_Graph - Зум](https://github.com/Storvild/resources/blob/master/img/wheellog_graph/002.jpg?raw=true)


Установка:   
    Если не установлен Python3, устанавливаем: [https://www.python.org/downloads/](https://www.python.org/downloads/)   
    Устанавливаем библиотеку matplotlib через командную строку:   
		pip install matplotlib==3.2.1    
    Запускаем файл wheellog_graph.py

Использование:    
	В Android-приложении Wheellog включаем логирование справа вверху (картинка похожая на молнию).    
    Для постоянного логирования на экране программы делаем свайп слева, открывается меню. Далее нажимаем настройка логирования/Автоматическое логирование - Вкл.   
 	Лог файлы сохраняются на андроид устройстве в папке Downloads/WheelLog Logs    
	После запуска Wheellog_Graph на компьютере, можно выбрать любой из csv файлов и далее анализировать графики скорости и мощности.

Программа протестирована на системах:    
	Windows7, Python 3.6, matplotlib=3.2.1    
	Windows10, Python 3.6, matplotlib=3.2.1    
	Linux Mint, Python 3.5, matplotlib=3.2.1    