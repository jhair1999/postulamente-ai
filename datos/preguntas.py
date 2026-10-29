def _pregunta(
    identificador,
    materia,
    tema,
    dificultad,
    enunciado,
    opciones,
    respuesta,
    explicacion,
    prerrequisitos,
    pistas,
    metodo
):
    return {
        "id": identificador,
        "materia": materia,
        "tema": tema,
        "nivel": dificultad,
        "dificultad": dificultad,
        "pregunta": enunciado,
        "opciones": opciones,
        "respuesta": respuesta,
        "explicacion": explicacion,
        "prerrequisitos": prerrequisitos,
        "pistas": pistas,
        "metodo": metodo
    }


PREGUNTAS = [
    _pregunta(
        1, "Álgebra", "Ecuaciones de primer grado", "Básico",
        "Si 2x + 6 = 16, ¿cuánto vale x?",
        ["3", "4", "5", "6"], "5",
        [
            "Restamos 6 a ambos lados: 2x = 10.",
            "Dividimos ambos lados entre 2.",
            "Obtenemos x = 5."
        ],
        ["Operaciones básicas", "Despeje de incógnitas"],
        ["Elimina primero el +6.", "Después divide entre 2."],
        "Despeje por operaciones inversas"
    ),
    _pregunta(
        2, "Álgebra", "Ecuaciones de primer grado", "Básico",
        "Si 3x - 4 = 11, ¿cuánto vale x?",
        ["4", "5", "6", "7"], "5",
        [
            "Sumamos 4 a ambos lados: 3x = 15.",
            "Dividimos ambos lados entre 3.",
            "Obtenemos x = 5."
        ],
        ["Operaciones básicas", "Despeje de incógnitas"],
        ["Usa la operación opuesta a restar 4.", "Divide 15 entre 3."],
        "Despeje por operaciones inversas"
    ),
    _pregunta(
        3, "Aritmética", "Porcentajes", "Básico",
        "¿Cuánto es el 20% de 150?",
        ["20", "25", "30", "35"], "30",
        [
            "20% significa 20/100, que equivale a 0.20.",
            "Multiplicamos 150 × 0.20.",
            "El resultado es 30."
        ],
        ["Fracciones", "Multiplicaciones", "Divisiones"],
        ["Convierte 20% en una fracción sobre 100.", "Multiplica por 150."],
        "Conversión de porcentaje a decimal"
    ),
    _pregunta(
        4, "Aritmética", "Fracciones", "Intermedio",
        "¿Cuánto es 3/4 + 1/8?",
        ["4/12", "5/8", "7/8", "1"], "7/8",
        [
            "El mínimo común denominador de 4 y 8 es 8.",
            "Convertimos 3/4 en 6/8.",
            "Sumamos 6/8 + 1/8 = 7/8."
        ],
        ["Múltiplos", "Fracciones equivalentes"],
        ["Usa un denominador común.", "3/4 equivale a 6/8."],
        "Suma con denominador común"
    ),
    _pregunta(
        5, "Aritmética", "Proporcionalidad", "Básico",
        "Si 5 cuadernos cuestan S/ 30, ¿cuánto cuestan 8 al mismo precio unitario?",
        ["S/ 40", "S/ 45", "S/ 48", "S/ 50"], "S/ 48",
        [
            "Cada cuaderno cuesta 30 ÷ 5 = 6 soles.",
            "Ocho cuadernos cuestan 8 × 6.",
            "El costo total es S/ 48."
        ],
        ["División", "Multiplicación"],
        ["Calcula primero el precio de uno.", "Multiplica ese precio por 8."],
        "Reducción a la unidad"
    ),
    _pregunta(
        6, "Aritmética", "Múltiplos", "Intermedio",
        "¿Cuál es el mínimo común múltiplo de 12 y 18?",
        ["24", "30", "36", "72"], "36",
        [
            "12 = 2² × 3 y 18 = 2 × 3².",
            "Tomamos cada factor con su mayor exponente: 2² × 3².",
            "2² × 3² = 4 × 9 = 36."
        ],
        ["Números primos", "Descomposición factorial"],
        ["Descompón ambos números en factores primos.", "Usa los mayores exponentes."],
        "Descomposición en factores primos"
    ),
    _pregunta(
        7, "Aritmética", "Porcentajes", "Intermedio",
        "Un precio sube de S/ 80 a S/ 100. ¿Cuál fue el aumento porcentual?",
        ["20%", "25%", "40%", "80%"], "25%",
        [
            "El aumento es 100 - 80 = 20.",
            "Comparamos el aumento con el precio inicial: 20/80.",
            "20/80 = 0.25 = 25%."
        ],
        ["Resta", "Fracciones", "Porcentajes"],
        ["Usa como base el precio inicial.", "Divide el aumento entre 80."],
        "Variación porcentual respecto del valor inicial"
    ),
    _pregunta(
        8, "Aritmética", "Promedios", "Básico",
        "¿Cuál es el promedio de 12, 15, 18, 25 y 30?",
        ["18", "20", "22", "25"], "20",
        [
            "Sumamos los cinco valores: 12 + 15 + 18 + 25 + 30 = 100.",
            "Dividimos la suma entre la cantidad de valores: 100 ÷ 5.",
            "El promedio es 20."
        ],
        ["Suma", "División"],
        ["Suma todos los datos.", "Divide entre 5, no entre el valor mayor."],
        "Media aritmética"
    ),
    _pregunta(
        9, "Álgebra", "Factorización", "Intermedio",
        "¿Cuáles son las soluciones de x² - 5x + 6 = 0?",
        ["1 y 6", "2 y 3", "-2 y -3", "3 y 5"], "2 y 3",
        [
            "Buscamos dos números cuyo producto sea 6 y cuya suma sea -5.",
            "Esos números son -2 y -3: (x - 2)(x - 3) = 0.",
            "Por ello, x = 2 o x = 3."
        ],
        ["Productos", "Propiedad del producto nulo"],
        ["Busca dos números que multipliquen 6.", "Las raíces hacen cero cada factor."],
        "Factorización de un trinomio mónico"
    ),
    _pregunta(
        10, "Álgebra", "Sistemas de ecuaciones", "Intermedio",
        "Si x + y = 10 y x - y = 4, ¿cuáles son x e y?",
        ["x = 6, y = 4", "x = 7, y = 3", "x = 8, y = 2", "x = 5, y = 5"],
        "x = 7, y = 3",
        [
            "Sumamos las ecuaciones y obtenemos 2x = 14.",
            "Entonces x = 7.",
            "Sustituimos en x + y = 10 y obtenemos y = 3."
        ],
        ["Ecuaciones de primer grado", "Suma de expresiones"],
        ["Suma ambas ecuaciones para eliminar y.", "Sustituye el valor de x."],
        "Método de eliminación"
    ),
    _pregunta(
        11, "Álgebra", "Expresiones algebraicas", "Intermedio",
        "Simplifica 3(2x - 1) - 2(x + 4).",
        ["4x - 11", "4x + 5", "8x - 5", "x - 11"], "4x - 11",
        [
            "Distribuimos: 3(2x - 1) = 6x - 3.",
            "Distribuimos el signo menos: -2(x + 4) = -2x - 8.",
            "Reducimos términos semejantes: 6x - 2x - 3 - 8 = 4x - 11."
        ],
        ["Propiedad distributiva", "Números negativos"],
        ["Distribuye ambos factores.", "Recuerda que -2 × 4 = -8."],
        "Propiedad distributiva y reducción de términos"
    ),
    _pregunta(
        12, "Álgebra", "Inecuaciones", "Intermedio",
        "Resuelve la inecuación 2x - 3 > 7.",
        ["x > 2", "x > 5", "x < 5", "x ≥ 5"], "x > 5",
        [
            "Sumamos 3 a ambos lados: 2x > 10.",
            "Dividimos entre 2, que es positivo, por lo que no cambia el signo.",
            "Obtenemos x > 5."
        ],
        ["Despeje", "Orden de números"],
        ["Aísla primero 2x.", "El signo solo cambia al dividir por un negativo."],
        "Despeje de inecuaciones"
    ),
    _pregunta(
        13, "Geometría", "Área de rectángulos", "Básico",
        "¿Cuál es el área de un rectángulo de 8 cm de largo y 5 cm de ancho?",
        ["13 cm²", "26 cm²", "40 cm²", "80 cm²"], "40 cm²",
        ["El área de un rectángulo es largo × ancho.", "8 × 5 = 40.", "El área es 40 cm²."],
        ["Multiplicación", "Unidades cuadradas"],
        ["No sumes los lados; eso daría parte del perímetro.", "Multiplica 8 por 5."],
        "Fórmula del área del rectángulo"
    ),
    _pregunta(
        14, "Geometría", "Área de triángulos", "Básico",
        "¿Cuál es el área de un triángulo con base 10 cm y altura 6 cm?",
        ["16 cm²", "30 cm²", "60 cm²", "120 cm²"], "30 cm²",
        ["Usamos A = base × altura ÷ 2.", "10 × 6 = 60.", "60 ÷ 2 = 30 cm²."],
        ["Multiplicación", "División"],
        ["El triángulo ocupa la mitad de un rectángulo equivalente.", "Divide el producto entre 2."],
        "Fórmula del área del triángulo"
    ),
    _pregunta(
        15, "Geometría", "Circunferencia", "Intermedio",
        "Usando π = 22/7, ¿cuál es la longitud de una circunferencia de radio 7 cm?",
        ["22 cm", "44 cm", "49 cm", "154 cm"], "44 cm",
        ["La longitud es L = 2πr.", "Sustituimos: 2 × (22/7) × 7.", "Se simplifica a 2 × 22 = 44 cm."],
        ["Fracciones", "Radio de una circunferencia"],
        ["Usa 2πr, no πr².", "El 7 del radio se simplifica con el denominador."],
        "Fórmula de longitud de circunferencia"
    ),
    _pregunta(
        16, "Geometría", "Teorema de Pitágoras", "Intermedio",
        "Un triángulo rectángulo tiene catetos de 6 cm y 8 cm. ¿Cuánto mide la hipotenusa?",
        ["10 cm", "12 cm", "14 cm", "15 cm"], "10 cm",
        ["Aplicamos c² = 6² + 8².", "c² = 36 + 64 = 100.", "c = √100 = 10 cm."],
        ["Potencias", "Raíz cuadrada"],
        ["La hipotenusa es el lado más largo.", "Suma los cuadrados de los catetos."],
        "Teorema de Pitágoras"
    ),
    _pregunta(
        17, "Geometría", "Polígonos regulares", "Intermedio",
        "¿Cuánto mide cada ángulo interior de un hexágono regular?",
        ["60°", "90°", "120°", "135°"], "120°",
        ["La suma interior es (n - 2) × 180°.", "Para n = 6: 4 × 180° = 720°.", "Como es regular, 720° ÷ 6 = 120°."],
        ["División", "Ángulos"],
        ["Primero calcula la suma de los seis ángulos.", "En un polígono regular todos son iguales."],
        "Suma de ángulos interiores"
    ),
    _pregunta(
        18, "Geometría", "Volumen de prismas", "Básico",
        "¿Cuál es el volumen de una caja rectangular de 3 cm, 4 cm y 5 cm?",
        ["12 cm³", "20 cm³", "47 cm³", "60 cm³"], "60 cm³",
        ["El volumen es largo × ancho × altura.", "3 × 4 × 5 = 60.", "El volumen es 60 cm³."],
        ["Multiplicación", "Unidades cúbicas"],
        ["Multiplica las tres dimensiones.", "El volumen se expresa en unidades cúbicas."],
        "Volumen de un prisma rectangular"
    ),
    _pregunta(
        19, "Trigonometría", "Razones trigonométricas", "Básico",
        "¿Cuál es el valor de sen 30°?",
        ["0", "1/2", "√2/2", "1"], "1/2",
        ["En un triángulo 30°-60°-90°, el lado opuesto a 30° es la mitad de la hipotenusa.", "sen 30° = opuesto/hipotenusa.", "Por tanto, sen 30° = 1/2."],
        ["Triángulos rectángulos", "Fracciones"],
        ["Recuerda el triángulo notable 30°-60°-90°.", "Seno es opuesto entre hipotenusa."],
        "Triángulo notable"
    ),
    _pregunta(
        20, "Trigonometría", "Razones trigonométricas", "Básico",
        "¿Cuál es el valor de cos 60°?",
        ["0", "1/2", "√3/2", "1"], "1/2",
        ["En un triángulo 30°-60°-90°, el cateto adyacente a 60° es la mitad de la hipotenusa.", "cos 60° = adyacente/hipotenusa.", "Por tanto, cos 60° = 1/2."],
        ["Triángulos rectángulos", "Fracciones"],
        ["Coseno es adyacente entre hipotenusa.", "Usa el triángulo notable."],
        "Triángulo notable"
    ),
    _pregunta(
        21, "Trigonometría", "Razones trigonométricas", "Básico",
        "¿Cuál es el valor de tan 45°?",
        ["0", "1/2", "1", "√3"], "1",
        ["En un triángulo 45°-45°-90°, los dos catetos son iguales.", "tan 45° = opuesto/adyacente.", "El cociente de dos longitudes iguales es 1."],
        ["Triángulos rectángulos", "División"],
        ["Tangente compara los dos catetos.", "En este triángulo los catetos son iguales."],
        "Triángulo notable"
    ),
    _pregunta(
        22, "Trigonometría", "Seno en triángulos", "Intermedio",
        "En un triángulo rectángulo, el cateto opuesto mide 6 y la hipotenusa 10. ¿Cuál es el seno del ángulo?",
        ["3/5", "4/5", "5/3", "5/4"], "3/5",
        ["Seno = cateto opuesto/hipotenusa.", "Sustituimos 6/10.", "Simplificamos entre 2 y obtenemos 3/5."],
        ["Fracciones", "Elementos del triángulo rectángulo"],
        ["Usa opuesto entre hipotenusa.", "Simplifica 6/10."],
        "Definición de seno"
    ),
    _pregunta(
        23, "Trigonometría", "Identidades trigonométricas", "Intermedio",
        "¿A qué es igual sen² θ + cos² θ?",
        ["0", "1", "tan θ", "2"], "1",
        ["Esta es la identidad pitagórica fundamental.", "Proviene de dividir a² + b² = c² entre c².", "Por ello, sen² θ + cos² θ = 1."],
        ["Teorema de Pitágoras", "Razones trigonométricas"],
        ["Es una identidad válida para todo ángulo donde se definen seno y coseno.", "Relaciona la expresión con Pitágoras."],
        "Identidad pitagórica"
    ),
    _pregunta(
        24, "Trigonometría", "Razones trigonométricas", "Intermedio",
        "Si tan θ = 3/4 y θ es agudo, ¿cuánto vale sen θ?",
        ["3/4", "3/5", "4/5", "5/4"], "3/5",
        ["Representamos los catetos como 3 y 4.", "La hipotenusa es √(3² + 4²) = 5.", "sen θ = opuesto/hipotenusa = 3/5."],
        ["Tangente", "Teorema de Pitágoras"],
        ["Dibuja un triángulo con catetos 3 y 4.", "Calcula la hipotenusa antes del seno."],
        "Construcción de un triángulo 3-4-5"
    ),
    _pregunta(
        25, "Razonamiento matemático", "Sucesiones", "Básico",
        "¿Qué número sigue en la sucesión 2, 5, 8, 11, ...?",
        ["12", "13", "14", "16"], "14",
        ["Calculamos las diferencias entre términos.", "Cada término aumenta en 3.", "11 + 3 = 14."],
        ["Suma", "Patrones"],
        ["Resta términos consecutivos.", "La diferencia es constante."],
        "Identificación de diferencia constante"
    ),
    _pregunta(
        26, "Razonamiento matemático", "Trabajo conjunto", "Intermedio",
        "Si 4 trabajadores terminan una obra en 6 días al mismo ritmo, ¿en cuántos días la harán 8 trabajadores?",
        ["2 días", "3 días", "6 días", "12 días"], "3 días",
        ["El trabajo total equivale a 4 × 6 = 24 jornadas-persona.", "Con 8 trabajadores dividimos 24 ÷ 8.", "La obra toma 3 días."],
        ["Multiplicación", "Proporcionalidad inversa"],
        ["Más trabajadores implican menos días.", "Mantén constante trabajadores × días."],
        "Proporcionalidad inversa"
    ),
    _pregunta(
        27, "Razonamiento matemático", "Edades", "Intermedio",
        "Ana tiene el doble de la edad de Luis y entre ambos suman 36 años. ¿Qué edades tienen?",
        ["Ana 18 y Luis 18", "Ana 20 y Luis 16", "Ana 24 y Luis 12", "Ana 30 y Luis 6"],
        "Ana 24 y Luis 12",
        ["Llamamos x a la edad de Luis; Ana tiene 2x.", "x + 2x = 36, entonces 3x = 36.", "Luis tiene 12 y Ana 24 años."],
        ["Ecuaciones de primer grado", "Multiplicación"],
        ["Representa la edad menor con x.", "Las edades son x y 2x."],
        "Planteamiento de una ecuación"
    ),
    _pregunta(
        28, "Razonamiento matemático", "Lógica", "Básico",
        "Todos los gatos son mamíferos. Mishi es un gato. ¿Qué conclusión es necesariamente verdadera?",
        ["Mishi vuela", "Mishi es mamífero", "Todos los mamíferos son gatos", "Mishi no es animal"],
        "Mishi es mamífero",
        ["La primera afirmación incluye a cada gato dentro del grupo de mamíferos.", "Mishi pertenece al grupo de los gatos.", "Entonces Mishi también pertenece al grupo de los mamíferos."],
        ["Clasificación", "Relaciones de inclusión"],
        ["Representa los gatos como un conjunto dentro de los mamíferos.", "Aplica la regla general al caso de Mishi."],
        "Deducción por inclusión de conjuntos"
    ),
    _pregunta(
        29, "Razonamiento matemático", "Sucesiones", "Básico",
        "¿Qué número sigue en la sucesión 1, 4, 9, 16, ...?",
        ["20", "24", "25", "32"], "25",
        ["Los términos son cuadrados perfectos: 1², 2², 3² y 4².", "El siguiente corresponde a 5².", "5² = 25."],
        ["Potencias", "Patrones"],
        ["Escribe cada término como una potencia de 2.", "Después de 4² viene 5²."],
        "Reconocimiento de cuadrados perfectos"
    ),
    _pregunta(
        30, "Razonamiento matemático", "Probabilidad", "Básico",
        "Al lanzar un dado justo de seis caras, ¿cuál es la probabilidad de obtener un número par?",
        ["1/6", "1/3", "1/2", "2/3"], "1/2",
        ["Los resultados posibles son 1, 2, 3, 4, 5 y 6.", "Los favorables son 2, 4 y 6: tres resultados.", "La probabilidad es 3/6 = 1/2."],
        ["Fracciones", "Conteo"],
        ["Cuenta los números pares entre 1 y 6.", "Divide casos favorables entre casos posibles."],
        "Regla de Laplace"
    )
]
