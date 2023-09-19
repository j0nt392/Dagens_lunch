En webscrape'r som hämtar veckans lunch från restaurang jöns jacob. 
Målet är att man i discord-gruppen ska kunna skriva ex "@dagenslunch" 
och då kunna se vilka 3 rätter som erbjuds på karolinska. 

Vad som inte är klart: 
Programmet ska kunna köras från discord genom att skriva t.ex "@lunch". Och 
helst borde programmet ligga på någon cloudserver så att det kan köras 24/7

Hur denna kan optimeras: 
-Istället för att använda RegEx för att tvätta bort HTML-kod, använd istället 
beautifulsoup metoder som är byggda för detta. 

Funktionalitet att lägga till: 
-Just nu hämtar "soup.findall()" alla recept för veckan. Istället vill vi 
kunna printa endast dagens lunch. 

-Det finns flera andra restauranger som tillhör karolinska man kanske vill 
kunna printa lunch från. 



