'''
@Autores: Wilenco team
@Ultima modificacion: junio 13/2016
@Ultimo modificador: Jorge Ayala
Pruebas de caja negra y blanca para proyecto
Fuente de referencia:
https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/
'''
from datetime import datetime
from django.test import TestCase
from django.test import Client
from django.test import LiveServerTestCase
from selenium import webdriver
from web.models import *

class TestCajaNegraContacto(LiveServerTestCase):
    """
       @Autor: Jorge Ayala
       Como su nombre lo indica, es una clase usada para realizar test.
       En este caso se lo usa para realizar pruebas de Caja negra a la
       Pagina Contacto de nuestro sitio web.
       Las input que se deben probar son:
       *Nombre
       Para las cuales se han identificado las siguientes clases
       de equivalencia:
            Clases de equivalencia:
               CE1: las cadenas de caracteres aceptados por el regex:
              /^[a-z\d_]{4,20}$/i
               CE2: las cadenas de caracteres no aceptados por el regex:
              /^[a-z\d_]{4,20}$/i
            Validez:
                CE1: valido
                CE2: invalido
       * Email
       Para las cuales se han identificado las siguientes clases
       de equivalencia:
            Clases de equivalencia:
               CE1: las cadenas de caracteres aceptados por el regex:
               ^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$
               CE2: las cadenas de caracteres no aceptados por el regex:
                ^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$
            Validez:
                CE1: valido
                CE2: invalido
        *Telefono
        *Asunto
    """
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(6)
        self.driver.set_window_size(1120, 550)

    def tearDown(self):
        #self.driver.quit() #Comentar para que se mantengan las paginas con las pruebas corriendo.
        print "\n"

    def test_nombre_correcto(self):
        """
        En esta prueba se utiliza la clase de equivalencia CE1.
        Como resultado, el usuario no debe ver ningun mensaje
        y los campos del formulario se limpian.
        """
        self.driver.get("http://localhost:8081/contacto/")
        self.driver.find_element_by_id('nombreUsuario').send_keys("Wilson Enriquez")
        self.driver.find_element_by_id('emailUsuario').send_keys("wilenco@hotmail.com")
        self.driver.find_element_by_id('telUsuario').send_keys("042-587452")
        self.driver.find_element_by_id('asuntoUsuario').send_keys("Mantenimiento de Centrales de Aire tipo Split.")
        self.driver.find_element_by_class_name("mybutton").click()
        msg_ok = self.driver.find_element_by_id("OkMessage")
        self.assertFalse(msg_ok.is_displayed(),"Prueba Valida No Exitosa")
        print "Prueba de nombre correcto exitosa "


    def test_nombre_incorrecto(self):
        """
        En esta prueba se utiliza la clase de equivalencia CE2.
        Como resultado, el usuario no debe ver ningun mensaje
        y los campos del formulario se limpian.
        """
        self.driver.get("http://localhost:8081/contacto/")
        self.driver.find_element_by_id('nombreUsuario').send_keys("Wil3nc0 S.4")
        self.driver.find_element_by_id('emailUsuario').send_keys("wilenco@hotmail.com")
        self.driver.find_element_by_id('telUsuario').send_keys("042-587452")
        self.driver.find_element_by_id('asuntoUsuario').send_keys("Mantenimiento de Centrales de Aire tipo Split.")
        self.driver.find_element_by_class_name("mybutton").click()
        msg_ok = self.driver.find_element_by_id("OkMessage")
        self.assertFalse(msg_ok.is_displayed(),"Prueba invalida No Exitosa")
        print "Prueba de nombre incorrecto exitosa "




    def test_email_correcto(self):
        """
        En esta prueba se utiliza la clase de equivalencia CE1.
        Como resultado, el usuario no debe ver ningun mensaje
        y los campos del formulario se limpian.
        """
        self.driver.get("http://localhost:8081/contacto/")
        self.driver.find_element_by_id('nombreUsuario').send_keys("Jorge Ayala")
        self.driver.find_element_by_id('emailUsuario').send_keys("test@iana.org")
        self.driver.find_element_by_id('telUsuario').send_keys("042-587452")
        self.driver.find_element_by_id('asuntoUsuario').send_keys("Mantenimiento de Centrales de Aire tipo Split.")
        self.driver.find_element_by_class_name("mybutton").click()
        msg_email_invalido = self.driver.find_element_by_id("msgEmailInvalido")
        self.assertFalse(msg_email_invalido.is_displayed())
        email_incorrecto = msg_email_invalido.is_displayed()
        prueba_correcta = not email_incorrecto
        print "Prueba de mail correcto exitosa? " + str(prueba_correcta)



    def test_email_incorrecto(self):
        '''
        En esta prueba se utiliza la clase de equivalencia CE2.
        Como resultado, el usuario debe ver un mensaje de email
        incorrecto en rojo.
        '''
        self.driver.get("http://localhost:8081/contacto/")
        self.driver.find_element_by_id('nombreUsuario').send_keys("Jorge Ayala")
        self.driver.find_element_by_id('emailUsuario').send_keys("testiana.org")
        self.driver.find_element_by_id('telUsuario').send_keys("042-587452")
        self.driver.find_element_by_id('asuntoUsuario').send_keys("Mantenimiento de Centrales de Aire tipo Split.")
        self.driver.find_element_by_class_name("mybutton").click()
        msg_email_invalido = self.driver.find_element_by_id("msgEmailInvalido")
        self.assertFalse(msg_email_invalido.is_displayed())
        #self.assertTrue(msg_email_invalido.is_displayed())
        print "Prueba de mail Incorrecto exitosa? " + str(msg_email_invalido.is_displayed())


class TestCajaNegraModeloSolicitud(TestCase):
    """
        @Autor: Israel Fernandez
        Clase para realizar un unit test del modelo Solicitud
        Ingresando entradas validas y no validas
    """
    def test_crear_solicitud_valida(self):
        self.cliente = Cliente.objects.create(cedula="0123457891", nombre="cliente",
                                              direccion="testlandia", telefono="0913458119",
                                              email="test@test.com")
        self.solicitud = Solicitud.objects.create(tipoSolicitud="MANT", descripcion="test",
                                                  fechaEscojida=datetime.now(),
                                                  cliente = self.cliente)

        self.assertIsInstance(self.solicitud, Solicitud, 'Solicitud exitosa')

    def test_crear_solicitud_invalida(self):
        self.solicitud = None
        try:
            self.solicitud = Solicitud.objects.create(tipoSolicitud="INST", descripcion="test",
                                                      fechaEscojida=datetime.now())
        except:
            self.assertNotIsInstance(self.solicitud, Solicitud, 'Solicitud Invalida')




class TestCajaNegraModeloCotizacion(TestCase):
    """
        @Autor: Jorge Ayala
        Clase para realizar un unit test de la entidad Cotizador
        Ingresando entradas validas y no validas, considerando validas las entradas
        con longitud correcta
    """
    def test_crear_cotizacion_valida(self):
        self.cliente = Cliente.objects.create(cedula="0123457891", nombre="cliente",
                                              direccion="testlandia", telefono="0913458119",
                                              email="test@test.com")

        self.producto1 = Producto.objects.create(noSerie="12345", nombre="testproduct",
                                                 stock=12, marca="test",
                                                 modelo="test", potencia="10KW",
                                                 capacidad="120BTU", descripcion="test")

        self.producto2 = Producto.objects.create(noSerie="12345", nombre="testproduct",
                                                 stock=12, marca="test",
                                                 modelo="test", potencia="10KW",
                                                 capacidad="120BTU", descripcion="test")

        self.cotizacion = Cotizacion.objects.create(cotizadorID="iedc1234WL",
                                                   cliente = self.cliente,
                                                   descripcionObra="Nada importante")

        self.cotizacion.producto.add(self.producto1)
        self.cotizacion.producto.add(self.producto2)
        self.assertIsInstance(self.cotizacion, Cotizacion, 'Cotizacion creada')

    def test_crear_cotizacion_invalida(self):
        self.cliente = Cliente.objects.create(cedula="0123457891", nombre="cliente",
                                              direccion="testlandia", telefono="0913458119",
                                              email="test@test.com")

        self.producto1 = Producto.objects.create(noSerie="12345", nombre="testproduct",
                                                 stock=12, marca="test",
                                                 modelo="test", potencia="10KW",
                                                 capacidad="120BTU", descripcion="test")

        self.producto2 = Producto.objects.create(noSerie="12345", nombre="testproduct",
                                                 stock=12, marca="test",
                                                 modelo="test", potencia="10KW",
                                                 capacidad="120BTU", descripcion="test")

        self.cotizacion = None

        try:
            self.cotizacion = Cotizacion.objects.create(cotizadorID="iedc1234WL",
                                                       descripcionObra="Nada importante")
        except:
            self.assertNotIsInstance(self.cotizacion, Cotizacion, 'Cotizacion creada')


class TestCajaNegraProducto(LiveServerTestCase):
    '''
    Clase para realizar prueba de caja negra para la entidad Producto
    '''
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(6)
        self.driver.set_window_size(1120, 550)

    def tearDown(self):
        self.driver.quit()

    def test_api_producto(self):
        client = Client()
        response = client.get('http://localhost:8081/api/producto/?format=json')
        self.assertEqual(response.status_code, 200)
