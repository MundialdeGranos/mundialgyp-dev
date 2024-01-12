from tkinter import Tk, Label, Entry, Button
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import date
import locale
import time

# Crear una instancia de WebDriver para el navegador Chrome
driver = webdriver.Chrome()

def esperar_elemento_presente(by, value, timeout=30):
    try:
        element_present = EC.presence_of_element_located((by, value))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f"Tiempo agotado para el elemento {value} no esta presente")

def iniciar_ejecucion():
    # Obtener la cantidad de repeticiones
    repeticiones = int(entry_repeticiones.get()) - 1

    initial_amount = int(entry_amount.get())

    # Cerrar la ventana
    ventana.destroy()

    # Navegar a la página de Odoo
    driver.get("https://www.mundialgyp.com/web/login") # pagina produccion
    #driver.get("https://mundialgyp-pruebas-13-12-23-10887145.dev.odoo.com/web/login") # pagina pruebas cambiar link al actual
    
    # Maximizar la ventana del navegador
    driver.maximize_window()    

    # Encontrar los campos de correo electrónico y contraseña 
    try:
        esperar_elemento_presente(By.NAME, 'login')
        email_field = driver.find_element(By.NAME, 'login')
        email_field.send_keys('mundialgyp14@gmail.com')
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys('miguel0331')

    # Encontrar y hacer clic en el botón de inicio de sesión
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
        submit_button.click()

    except Exception as e:
        print(f"Error: {e}")
    
    # Hacer clic en contabilidad
    botones = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "o_caption"))
    )

    # Buscar el botón con el texto "punto de venta"
    for boton in botones:
        if boton.text == "Contabilidad":
            # Dar clic al botón
            boton.click()
            break    

    # Realizar el filtro en favoritos
    dropdown_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[@class='o_dropdown_title'][text()='Favoritos']")))
    dropdown_title.click()
    time.sleep(2)
    # Click en el filtro de "CIPA"
    filtro_cipa = driver.find_element(By.XPATH, "//span[contains(text(),'cipa')]")
    filtro_cipa.click()
    time.sleep(2)
    # Clic en los tres puntos del diario cipa
    cipa = driver.find_element(By.CSS_SELECTOR, "button.o_kanban_manage_toggle_button")
    cipa.click()
    time.sleep(1)
    # clic en trasnferencia interna
    transferencia_interna = driver.find_element(By.LINK_TEXT,'Transferencia interna')
    transferencia_interna.click()
    time.sleep(2)
    # Clic en recibir en el tipo de trasnferencia 
    recibir = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//label[contains(text(), 'Recibir')]")))
    recibir.click()    
    # buscar el campo amount y llenar sus valores con el inicial
    campo_importe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'amount')))
    time.sleep(2)
    campo_importe.clear()
    time.sleep(2)
    campo_importe.send_keys(str(initial_amount))    
    # clic en diario de destino y llenar sus valores de banco
    campo_destino = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'destination_journal_id')))    
    campo_destino.clear()   
    campo_destino.send_keys('BANCOL 13988 CORRESP')  
    time.sleep(2) 
    campo_destino.send_keys(Keys.RETURN)    
    # Clic en el campo de memo para asignar la refencia de la transferencia interna con la fecha
    campo_memo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'ref')))
    campo_memo.clear()
    locale.setlocale(locale.LC_ALL, 'es_ES') 
    fecha_actual = date.today()
    fecha_formateada = fecha_actual.strftime("%d de %B de %Y").upper() 
    texto_memo = f'BANCOLOMBIA {fecha_formateada} PLAZA MAYORISTA'
    campo_memo.send_keys(texto_memo)
    time.sleep(2)
    # clic en confirmar transferencia
    boton_confirmar = driver.find_element(By.XPATH, "//button[@name='action_post']")
    boton_confirmar.click()
    time.sleep(2)
    # inicio de repeticiones en el bucle
    for _ in range(repeticiones):
        # Click en accion
        time.sleep(2)
        element_accion = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='o_dropdown_title'][contains(text(),'Acción')]")))
        element_accion.click()
        time.sleep(2)

        # Obtener el elemento de menú "duplicar" y hacer clic en él    
        element_duplicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Duplicar')]")))
        element_duplicar.click()
        time.sleep(2)
        campo_importe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'amount')))
        importe_actual_str = campo_importe.get_attribute("value")
        importe_actual_str = importe_actual_str.replace(".", "")
        importe_actual_str = importe_actual_str.split(",")[0]
        importe_actual = int(importe_actual_str) 
        nuevo_importe = importe_actual - 1
        campo_importe.clear() 
        time.sleep(2)       
        campo_importe.send_keys(str(nuevo_importe))    
        campo_memo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'ref')))
        campo_memo.clear()
        locale.setlocale(locale.LC_ALL, 'es_ES')    
        fecha_actual = date.today()
        fecha_formateada = fecha_actual.strftime("%d de %B de %Y").upper()
        texto_memo = f'BANCOLOMBIA {fecha_formateada} PLAZA MAYORISTA'
        campo_memo.send_keys(texto_memo)
        time.sleep(2)
        boton_confirmar = driver.find_element(By.XPATH, "//button[@name='action_post']")
        boton_confirmar.click()
        time.sleep(5)
    # Cerrar el navegador al finalizar la automatización
    driver.quit()

    # Mostrar mensaje indicando la finalización de la automatización
    messagebox.showinfo("Finalizado", "La automatización de transferencias ha sido completada. Revisar ODOO")

# Crear la ventana emergente cantidad de recibos 
ventana = Tk()
ventana.title("Transferencias internas")
ventana.geometry("300x150")

# Etiqueta y entrada para la cantidad de transferencias
label_repeticiones = Label(ventana, text="Cantidad de Transferencias:")
label_repeticiones.pack()
entry_repeticiones = Entry(ventana)
entry_repeticiones.pack()

# Crear la ventana emergente cantidad de recibos
label_amount = Label(ventana, text="Valor recibo inicial:")
label_amount.pack()

# Etiqueta y entrada para el valor inicial
entry_amount = Entry(ventana)
entry_amount.pack()

# Botón para iniciar la ejecución de la automatización
boton_ejecutar = Button(ventana, text="Iniciar", command=iniciar_ejecucion)
boton_ejecutar.pack()

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
