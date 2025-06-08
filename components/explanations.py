"""
Componente para crear explicaciones detalladas de las secciones del dashboard.
Ayuda a los usuarios a entender qué significan los datos y gráficos.
"""

import streamlit as st


def create_explanation_section(section_type: str):
    """
    Crea una sección de explicación para cada tipo de análisis
    
    Args:
        section_type: Tipo de sección ('hero_analysis', 'rankings_players', 'rankings_heroes', 
                     'time_analysis', 'professional', 'data_exploration', 'composition', 'advanced')
    """
    
    explanations = {
        'hero_analysis': {
            'title': '📖 ¿Cómo interpretar el Análisis de Héroes?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Este análisis te muestra el rendimiento de diferentes héroes en Heroes of the Storm, basado en las partidas registradas.
            
            ### 📊 **Gráficos y su significado:**
            
            **🔸 Gráfico de Barras - Rendimiento por Héroe:**
            - **Eje X (horizontal):** Nombres de los héroes
            - **Eje Y (vertical):** Valor de la métrica seleccionada
            - **Barras más altas:** Mejor rendimiento en esa métrica
            
            **🔸 Métricas disponibles y qué significan:**
            - **HeroKills:** Eliminaciones de héroes enemigos (más = mejor jugador de combate)
            - **Deaths:** Muertes del héroe (menos = mejor supervivencia)
            - **Assists:** Asistencias en eliminaciones (más = mejor trabajo en equipo)
            - **HeroDamage:** Daño total infligido a héroes enemigos (más = mayor impacto en combate)
            - **Healing:** Curación realizada a aliados (más = mejor soporte)
            - **SiegeDamage:** Daño a estructuras enemigas (más = mejor en objetivos)
            
            ### 🔍 **Cómo usar esta información:**
            
            1. **Para elegir héroe:** Busca héroes con alto rendimiento en métricas importantes
            2. **Para mejorar tu juego:** Compara tu rendimiento con los promedios mostrados
            3. **Para entender el meta:** Los héroes con mejores estadísticas suelen ser más efectivos
            4. **Para formar equipos:** Combina héroes que se complementen en diferentes métricas
            
            ### ⚠️ **Consideraciones importantes:**
            
            - Los datos reflejan el rendimiento promedio, no garantizan resultados individuales
            - Algunos héroes pueden tener pocas partidas registradas (menos confiables)
            - El contexto de la partida (composición, mapa, duración) afecta las estadísticas
            - Las métricas deben interpretarse según el rol del héroe (tank, support, damage, etc.)
            """
        },
          'rankings_players': {
            'title': '🏆 ¿Cómo interpretar los Rankings de Jugadores?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Esta sección muestra el ranking de los mejores jugadores basado en diferentes métricas de rendimiento, incluyendo el héroe con el que lograron su mejor performance.
            
            ### 📊 **Tablas de Rankings:**
            
            **🔸 Estructura de la tabla:**
            - **Posición:** Ranking del jugador (1 = mejor)
            - **Jugador:** Nombre/ID del jugador
            - **Héroe:** El héroe con el que logró ese ranking (nuevo!)
            - **Valor:** Puntuación en la métrica seleccionada
            
            **🔸 Información del héroe mostrado:**
            - **Modo Promedio:** Héroe más usado por el jugador en esa métrica
            - **Modo Total:** Héroe que más contribuyó al total acumulado
            - **Modo Máximo:** Héroe con el que logró el mejor registro individual
            
            **🔸 Métricas de evaluación:**
            - **Promedio por partida:** Rendimiento consistente del jugador
            - **Total acumulado:** Suma total de todas las partidas
            - **Máximo:** El mejor registro individual alcanzado
            
            ### 🎖️ **Tipos de métricas explicadas:**
            
            **💀 Combate:**
            - **Eliminaciones:** Héroes enemigos eliminados
            - **Asistencias:** Participación en eliminaciones de equipo
            - **Takedowns:** Eliminaciones + Asistencias combinadas
            
            **🛡️ Supervivencia:**
            - **Muertes:** Veces que el jugador murió (menos es mejor)
            - **Daño Recibido:** Capacidad de absorber daño
            
            **⚔️ Impacto:**
            - **Daño a Héroes:** Contribución directa al combate
            - **Curación:** Soporte brindado al equipo
            - **Daño a Estructuras:** Contribución a objetivos
            
            ### 🔍 **Cómo interpretar los resultados:**
            
            1. **Top Players:** Los primeros lugares son consistentemente buenos
            2. **Especialización por héroe:** Cada jugador tiene héroes favoritos/exitosos
            3. **Diversidad:** Algunos jugadores destacan con múltiples héroes
            4. **Contexto del rol:** El héroe mostrado indica el estilo de juego preferido
            
            ### 💡 **Consejos para usar esta información:**
            
            - **Buscar mentores:** Estudia a los mejores jugadores y sus héroes preferidos
            - **Aprender builds:** Investiga los talentos/estrategias de estos jugadores
            - **Encontrar tu héroe:** Ve qué héroes usan los mejores en cada métrica
            - **Establecer metas:** Usa los valores como objetivos de mejora
            - **Inspiración:** Prueba los héroes que usan los mejores jugadores
            """
        },
        
        'rankings_heroes': {
            'title': '🦸‍♂️ ¿Cómo interpretar los Rankings de Héroes?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Este ranking muestra qué héroes tienen el mejor rendimiento promedio en diferentes aspectos del juego.
            
            ### 📊 **Interpretación de las tablas:**
            
            **🔸 Columnas principales:**
            - **Posición:** Ranking del héroe (1 = mejor rendimiento)
            - **Héroe:** Nombre del personaje
            - **Promedio:** Valor promedio de la métrica por partida
            - **Partidas:** Número de veces jugado (sample size)
            - **Total:** Suma acumulada de todas las partidas
            
            ### 🎮 **Categorías de héroes y sus métricas clave:**
            
            **⚔️ Assassins/Damage Dealers:**
            - **HeroKills:** Eliminaciones (objetivo: >3 por partida)
            - **HeroDamage:** Daño a héroes (objetivo: >40,000 por partida)
            - **SiegeDamage:** Daño a estructuras (objetivo: >30,000 por partida)
            
            **🛡️ Tanks/Warriors:**
            - **DamageTaken:** Daño absorbido (más es mejor para tanques)
            - **TimeCCdEnemyHeroes:** Control de masas aplicado
            - **Assists:** Participación en eliminaciones del equipo
            
            **💚 Supports/Healers:**
            - **Healing:** Curación total (objetivo: >20,000 por partida)
            - **Assists:** Asistencias (objetivo: >10 por partida)
            - **Deaths:** Muertes (menos es mejor, objetivo: <3 por partida)
            
            **🏗️ Specialists:**
            - **SiegeDamage:** Presión sobre estructuras
            - **ExperienceContribution:** Contribución de experiencia
            - **MinionDamage:** Limpieza de oleadas
            
            ### 📈 **Cómo leer los datos:**
            
            **🔸 Héroes con pocas partidas (<5):**
            - Datos menos confiables
            - Pueden ser outliers o situaciones específicas
            
            **🔸 Héroes con muchas partidas (>20):**
            - Datos más confiables y representativos
            - Reflejan el rendimiento típico del héroe
            
            **🔸 Valores extremos:**
            - Muy altos: Héroe muy efectivo en esa métrica
            - Muy bajos: Puede ser debilidad o rol diferente
            
            ### 🎯 **Aplicaciones prácticas:**
            
            1. **Selección de héroes:** Elige héroes con buen rendimiento general
            2. **Bans estratégicos:** Banea héroes dominantes del meta
            3. **Contraselección:** Evita héroes con bajo rendimiento
            4. **Aprendizaje:** Practica con héroes que tienen potencial alto
            5. **Formación de equipo:** Combina héroes complementarios
            
            ### ⚠️ **Advertencias importantes:**
            
            - **Contexto del parche:** Los datos pueden no reflejar cambios recientes
            - **Nivel de juego:** Héroes efectivos en pro pueden no serlo en casual
            - **Composición:** Algunos héroes necesitan sinergias específicas
            - **Mapa dependiente:** Ciertos héroes son mejores en mapas específicos
            """
        },
        
        'time_analysis': {
            'title': '📈 ¿Cómo interpretar el Análisis de Tendencias Temporales?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Esta sección analiza cómo han evolucionado las métricas de juego a lo largo del tiempo, mostrando tendencias y patrones.
            
            ### 📊 **Tipos de gráficos temporales:**
            
            **🔸 Gráfico de líneas temporal:**
            - **Eje X:** Tiempo (fechas, semanas, meses)
            - **Eje Y:** Valor de la métrica
            - **Línea ascendente:** Mejora o aumento en el tiempo
            - **Línea descendente:** Decline o reducción
            - **Línea plana:** Estabilidad en el rendimiento
            
            **🔸 Gráfico de barras por período:**
            - Compara valores entre diferentes períodos de tiempo
            - Útil para ver cambios estacionales o por patches
            
            ### 📅 **Períodos de análisis:**
            
            **🔹 Análisis diario:**
            - Muestra variaciones día a día
            - Útil para identificar patrones de actividad
            - Puede mostrar días de la semana más activos
            
            **🔹 Análisis semanal:**
            - Promedia el rendimiento por semana
            - Suaviza las variaciones diarias
            - Mejor para ver tendencias generales
            
            **🔹 Análisis mensual:**
            - Tendencias a largo plazo
            - Impacto de actualizaciones o eventos especiales
            - Evolución general del meta
            
            ### 🔍 **Métricas temporales importantes:**
            
            **📈 Rendimiento promedio:**
            - Evolución del skill level general
            - Impacto del aprendizaje y práctica
            - Efectos de cambios en el juego
            
            **🎮 Actividad de juego:**
            - Número de partidas por período
            - Picos de actividad (eventos, weekends)
            - Tendencias de popularidad
            
            **⚖️ Balance del juego:**
            - Cambios en efectividad de héroes
            - Impacto de buffs/nerfs
            - Evolución del meta competitivo
            
            ### 🎯 **Cómo interpretar las tendencias:**
            
            **📊 Tendencias ascendentes:**
            - **En rendimiento:** Mejora general del skill
            - **En actividad:** Mayor popularidad o eventos
            - **En métricas específicas:** Posibles cambios de balance
            
            **📉 Tendencias descendentes:**
            - **En rendimiento:** Puede indicar cambios difíciles de adaptar
            - **En actividad:** Menor interés o competencia externa
            - **En efectividad:** Nerfs o cambios negativos
            
            **➡️ Tendencias estables:**
            - Balance saludable del juego
            - Consistencia en el rendimiento
            - Meta establecido y conocido
            
            ### 💡 **Aplicaciones prácticas:**
            
            1. **Timing de práctica:** Identifica cuándo juegas mejor
            2. **Selección de héroes:** Ve qué héroes están en tendencia positiva
            3. **Planificación:** Entiende ciclos de actividad para eventos
            4. **Adaptación:** Ajústate a cambios de meta mostrados en tendencias
            
            ### ⚠️ **Consideraciones importantes:**
            
            - **Sample size:** Períodos con pocas partidas son menos confiables
            - **Eventos externos:** Holidays, patches, y eventos afectan los datos
            - **Correlación vs Causalidad:** Las tendencias no siempre implican causa directa
            - **Contexto del juego:** Cambios en el juego pueden crear discontinuidades
            """
        },
        
        'professional': {
            'title': '🚀 ¿Cómo interpretar los Analytics Profesionales?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Esta sección presenta análisis avanzados típicos del juego profesional y competitivo de alto nivel.
            
            ### 📊 **Métricas profesionales explicadas:**
            
            **🔸 KDA (Kill/Death/Assist Ratio):**
            - **Fórmula:** (Kills + Assists) / Deaths
            - **>2.0:** Excelente rendimiento
            - **1.5-2.0:** Buen rendimiento
            - **<1.0:** Necesita mejorar
            
            **🔸 Damage Share:**
            - **Qué es:** Porcentaje del daño total del equipo
            - **DPS esperado:** 25-35% del daño del equipo
            - **Tanks:** 15-25%
            - **Supports:** 5-15%
            
            **🔸 Efficiency Metrics:**
            - **Damage per Minute:** Daño promedio por minuto de juego
            - **Healing per Minute:** Curación promedio por minuto
            - **Experience per Minute:** Contribución de XP por minuto
            
            ### 🏆 **Análisis de rendimiento por rol:**
            
            **⚔️ Damage Dealers (Assassins):**
            - **Prioridad #1:** Alto Hero Damage y Kills
            - **Objetivo:** >40k Hero Damage por partida
            - **KDA objetivo:** >2.0
            - **Participación:** >60% de las eliminaciones del equipo
            
            **🛡️ Tanks (Warriors):**
            - **Prioridad #1:** Alto Damage Taken y Assists
            - **Objetivo:** >50k Damage Taken por partida
            - **Supervivencia:** <4 muertes por partida
            - **Iniciación:** Alto Time CC'd Enemy Heroes
            
            **💚 Supports (Healers):**
            - **Prioridad #1:** Alta Healing y baja Deaths
            - **Objetivo:** >25k Healing por partida
            - **Supervivencia:** <3 muertes por partida
            - **Asistencias:** >70% de las eliminaciones del equipo
            
            **🏗️ Specialists:**
            - **Prioridad #1:** Alto Siege Damage y Experience
            - **Objetivo:** Varía según el héroe específico
            - **Contribución única:** Métricas especiales según habilidades
            
            ### 📈 **Gráficos avanzados:**
            
            **🔸 Radar Charts (Gráficos de araña):**
            - Muestran múltiples métricas simultáneamente
            - Área mayor = mejor rendimiento general
            - Forma equilibrada = jugador completo
            - Picos específicos = especialización
            
            **🔸 Heat Maps:**
            - Intensidad de color = nivel de rendimiento
            - Rojo intenso = excelente
            - Azul/frío = necesita mejora
            - Patrones claros = consistencia
            
            **🔸 Correlation Analysis:**
            - Muestra relaciones entre métricas
            - Correlación positiva = métricas que suben juntas
            - Correlación negativa = relación inversa
            - Útil para entender trade-offs
            
            ### 🎯 **Benchmarking profesional:**
            
            **🏅 Tier List basada en datos:**
            - **S-Tier:** Top 10% de rendimiento
            - **A-Tier:** Top 25% de rendimiento
            - **B-Tier:** Promedio (25-75%)
            - **C-Tier:** Bottom 25%
            
            **📊 Percentiles:**
            - **95th percentile:** Elite level
            - **75th percentile:** Above average
            - **50th percentile:** Average
            - **25th percentile:** Below average
            
            ### 💡 **Cómo usar estos análisis:**
            
            1. **Auto-evaluación:** Compara tu rendimiento con benchmarks
            2. **Identificar fortalezas:** Ve en qué métricas destacas
            3. **Encontrar debilidades:** Identifica áreas de mejora
            4. **Establecer objetivos:** Usa percentiles como metas
            5. **Análisis de equipo:** Evalúa balance de roles en tu equipo
            
            ### 🔬 **Interpretación avanzada:**
            
            **🔸 Context-aware analysis:**
            - Duración de partida afecta todas las métricas
            - Composición de equipo influye en roles individuales
            - Mapas específicos favorecen diferentes estrategias
            
            **🔸 Meta considerations:**
            - Datos históricos pueden no reflejar meta actual
            - Cambios de balance alteran efectividad relativa
            - Pro play vs Ranked vs Casual tienen metas diferentes
            
            ### ⚠️ **Limitaciones importantes:**
            
            - Los datos no capturan decision-making o macro play
            - Métricas individuales no muestran teamwork
            - Sample size pequeño puede sesgar resultados
            - Contexto específico de cada partida es crucial
            """
        },
        
        'data_exploration': {
            'title': '🔍 ¿Cómo interpretar la Exploración de Datos?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Esta sección te permite explorar libremente los datos del juego usando diferentes filtros y visualizaciones.
            
            ### 📊 **Herramientas de exploración:**
            
            **🔸 Filtros dinámicos:**
            - **Por héroe:** Analiza rendimiento de héroes específicos
            - **Por jugador:** Ve estadísticas de jugadores particulares
            - **Por fecha:** Examina períodos específicos
            - **Por métrica:** Enfócate en aspectos específicos del juego
            
            **🔸 Visualizaciones interactivas:**
            - **Scatter plots:** Relaciones entre dos métricas
            - **Histogramas:** Distribución de valores
            - **Box plots:** Rangos y outliers
            - **Tablas dinámicas:** Datos tabulares detallados
            
            ### 🔍 **Tipos de análisis exploratorio:**
            
            **📈 Análisis univariado:**
            - Examina una métrica a la vez
            - Distribución de valores (normal, sesgada, etc.)
            - Valores típicos, extremos y outliers
            - Tendencia central (promedio, mediana)
            
            **📊 Análisis bivariado:**
            - Relación entre dos métricas
            - Correlaciones positivas/negativas
            - Patrones y agrupaciones
            - Causas y efectos potenciales
            
            **🔄 Análisis multivariado:**
            - Múltiples métricas simultáneamente
            - Patrones complejos y interacciones
            - Segmentación de jugadores/héroes
            - Perfiles de rendimiento
            
            ### 📋 **Interpretación de estadísticas descriptivas:**
            
            **🔸 Medidas de tendencia central:**
            - **Media (promedio):** Valor típico, afectado por outliers
            - **Mediana:** Valor central, resistente a outliers
            - **Moda:** Valor más frecuente
            
            **🔸 Medidas de dispersión:**
            - **Desviación estándar:** Qué tan dispersos están los datos
            - **Rango:** Diferencia entre máximo y mínimo
            - **Percentiles:** Posición relativa de valores
            
            **🔸 Medidas de forma:**
            - **Asimetría:** Si los datos se inclinan hacia un lado
            - **Curtosis:** Qué tan "puntiaguda" es la distribución
            
            ### 🎮 **Aplicaciones prácticas en gaming:**
            
            **🔹 Identificar patrones:**
            - ¿Qué héroes funcionan bien juntos?
            - ¿Qué métricas predicen victoria?
            - ¿Hay combinaciones estratégicas efectivas?
            
            **🔹 Detectar anomalías:**
            - Partidas con rendimiento extremo
            - Jugadores con estadísticas inusuales
            - Héroes con comportamiento atípico
            
            **🔹 Optimización de estrategias:**
            - Mejores picks según situación
            - Métricas más importantes para ganar
            - Debilidades comunes a explotar
            
            ### 🔬 **Técnicas de análisis avanzado:**
            
            **🔸 Clustering (Agrupamiento):**
            - Agrupa jugadores/héroes similares
            - Identifica arquetipos de juego
            - Encuentra nichos estratégicos
            
            **🔸 Outlier Detection:**
            - Identifica valores extremos
            - Puede indicar errores o situaciones especiales
            - Útil para encontrar jugadores excepcionales
            
            **🔸 Correlation Analysis:**
            - Qué métricas tienden a subir/bajar juntas
            - Relaciones fuertes vs débiles
            - Correlación vs causalidad
            
            ### 💡 **Consejos para exploración efectiva:**
            
            1. **Comienza con preguntas específicas:** "¿Qué hace efectivo a este héroe?"
            2. **Usa múltiples visualizaciones:** Diferentes gráficos revelan diferentes patrones
            3. **Filtra progresivamente:** Empieza amplio, luego específico
            4. **Busca outliers:** Los valores extremos son informativos
            5. **Valida hallazgos:** Confirma patrones con diferentes subsets de datos
            
            ### 🎯 **Interpretación de resultados:**
            
            **🔸 Patrones consistentes:**
            - Se repiten en diferentes subsets
            - Probablemente reflejan mecánicas del juego
            - Confiables para tomar decisiones
            
            **🔸 Patrones inconsistentes:**
            - Aparecen solo en casos específicos
            - Pueden ser casualidad o contexto específico
            - Requieren más investigación
            
            **🔸 No-patrones (ruido):**
            - Distribución aleatoria
            - Sin correlaciones claras
            - Puede indicar que esa métrica no es predictiva
            
            ### ⚠️ **Precauciones importantes:**
            
            - **Correlation ≠ Causation:** Relación no implica causa
            - **Sample bias:** Datos pueden no ser representativos
            - **Overfitting:** No generalizar de muestras pequeñas
            - **Context matters:** Situación específica afecta interpretación
            - **Temporal changes:** Datos antiguos pueden no aplicar actualmente
            """
        },
        
        'composition': {
            'title': '📋 ¿Cómo interpretar el Análisis de Composiciones?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Esta sección analiza las composiciones de equipo más efectivas y cómo diferentes combinaciones de héroes funcionan juntas.
            
            ### 🏗️ **Conceptos fundamentales de composiciones:**
            
            **🔸 Roles básicos en Heroes of the Storm:**
            - **Tank:** Inicia peleas, absorbe daño, protege al equipo
            - **Bruiser:** Daño sostenido, tanqueo secundario
            - **Ranged Assassin:** Daño a distancia, elimina objetivos prioritarios
            - **Melee Assassin:** Daño cuerpo a cuerpo, elimina objetivos aislados
            - **Support:** Curación, buffs, utilidad para el equipo
            - **Specialist:** Roles únicos, presión en lanes, utilidad específica
            
            **🔸 Meta-composiciones típicas:**
            - **Standard:** Tank + Support + 3 DPS
            - **Double Support:** Tank + 2 Supports + 2 DPS
            - **Double Tank:** 2 Tanks + Support + 2 DPS
            - **Poke Comp:** Enfoque en daño a distancia
            - **Dive Comp:** Enfoque en eliminar objetivos específicos
            - **Sustain Comp:** Enfoque en supervivencia y peleas largas
            
            ### 📊 **Métricas de composición:**
            
            **🔸 Sinergias de equipo:**
            - **Win Rate:** Porcentaje de victorias de la composición
            - **Average Game Length:** Duración promedio de partidas
            - **Team Fight Win Rate:** Éxito en peleas de equipo
            - **Objective Control:** Control de objetivos del mapa
            
            **🔸 Distribución de roles:**
            - Porcentaje de cada rol en composiciones exitosas
            - Balance óptimo entre tanque, daño y soporte
            - Flexibilidad vs especialización
            
            ### 🎮 **Análisis de efectividad:**
            
            **🔸 Gráficos de win rate por composición:**
            - **Eje X:** Diferentes composiciones de equipo
            - **Eje Y:** Porcentaje de victorias
            - **Barras más altas:** Composiciones más exitosas
            - **Tamaño de muestra:** Número de partidas con esa composición
            
            **🔸 Heat maps de sinergias:**
            - **Filas/Columnas:** Diferentes héroes
            - **Color:** Efectividad cuando juegan juntos
            - **Rojo/Caliente:** Muy buena sinergia
            - **Azul/Frío:** Pobre sinergia o anti-sinergia
            
            ### 🔄 **Tipos de sinergias:**
            
            **🔸 Sinergias ofensivas:**
            - **Wombo combos:** Combinaciones de ultimates devastadoras
            - **Chain CC:** Control de masas encadenado
            - **Focus fire:** Concentración de daño en objetivos
            - **Ejemplo:** Malf root + Jaina combo
            
            **🔸 Sinergias defensivas:**
            - **Peeling:** Protección de carries vulnerables
            - **Sustain:** Curación y mitigación de daño combinada
            - **Disengage:** Herramientas para escapar de peleas malas
            - **Ejemplo:** Tassadar shield + Uther armor
            
            **🔸 Sinergias de map control:**
            - **Split push:** Presión en múltiples lanes
            - **Objective control:** Dominancia en objetivos específicos
            - **Vision control:** Information warfare
            - **Rotations:** Movimiento coordinado de equipo
            
            ### 📈 **Interpretación de gráficos:**
            
            **🔸 Composición win rate charts:**
            - **>60% win rate:** Muy fuerte, probablemente meta
            - **50-60% win rate:** Viable, depende de ejecución
            - **40-50% win rate:** Débil, requiere ventajas específicas
            - **<40% win rate:** Evitar, probablemente tiene counters duros
            
            **🔸 Role distribution pie charts:**
            - Muestra el balance ideal de roles
            - Desviaciones pueden indicar metas específicos
            - Útil para entender qué roles son prioritarios
            
            ### 🎯 **Estrategias de draft:**
            
            **🔸 Pick phase priorities:**
            1. **First picks:** Héroes flexibles, difíciles de counter
            2. **Middle picks:** Completar core de la composición
            3. **Last picks:** Counterpicks y ajustes finales
            
            **🔸 Ban considerations:**
            - **Power bans:** Héroes dominantes del meta
            - **Target bans:** Contra especialidades del oponente
            - **Synergy bans:** Prevenir combos específicos
            - **Flex bans:** Reducir opciones flexibles del enemigo
            
            ### 💡 **Aplicaciones prácticas:**
            
            **🔹 En draft ranked:**
            1. Identifica composiciones fuertes del meta actual
            2. Aprende 2-3 composiciones bien
            3. Practica sinergias específicas con tu equipo
            4. Reconoce win conditions de cada composición
            
            **🔹 Como jugador individual:**
            1. Aprende múltiples roles para flexibilidad
            2. Entiende tu función en diferentes composiciones
            3. Comunica picks y estrategia con el equipo
            4. Adapta tu estilo de juego a la composición
            
            **🔹 Análisis post-partida:**
            1. ¿La composición fue apropiada para el mapa?
            2. ¿Se ejecutaron las sinergias correctamente?
            3. ¿Qué composición enemiga nos causó problemas?
            4. ¿Cómo podríamos mejorar nuestro draft?
            
            ### ⚠️ **Consideraciones importantes:**
            
            **🔸 Dependencia del mapa:**
            - Algunos mapas favorecen composiciones específicas
            - Objetivos del mapa influyen en efectividad
            - Estructura del mapa afecta viabilidad de estrategias
            
            **🔸 Skill floor vs skill ceiling:**
            - Composiciones fáciles vs difíciles de ejecutar
            - Algunas requieren coordinación perfecta
            - Nivel de juego afecta viabilidad
            
            **🔸 Meta evolution:**
            - Los datos históricos pueden no reflejar meta actual
            - Parches cambian balance y viabilidad
            - Innovación puede crear nuevas composiciones efectivas
            
            **🔸 Sample size warnings:**
            - Composiciones raras pueden tener datos insuficientes
            - High win rate con pocas partidas no es confiable
            - Busca consistencia en múltiples períodos
            
            ### 🏆 **Objetivos de aprendizaje:**
            
            1. **Reconocer** composiciones meta efectivas
            2. **Entender** por qué ciertas combinaciones funcionan
            3. **Ejecutar** sinergias específicas en partidas
            4. **Adaptar** estrategia según composición propia y enemiga
            5. **Innovar** encontrando nuevas combinaciones efectivas
            """
        },
        
        'advanced': {
            'title': '🎯 ¿Cómo interpretar las Métricas Avanzadas?',
            'content': """
            ### 🎯 **¿Qué estás viendo aquí?**
            
            Esta sección presenta análisis estadísticos avanzados y métricas complejas para jugadores que buscan insights profundos.
            
            ### 🔬 **Métricas estadísticas avanzadas:**
            
            **🔸 Z-Scores (Puntuaciones estándar):**
            - **Qué es:** Mide cuántas desviaciones estándar está un valor del promedio
            - **Z > 2:** Excepcional (top 2.5%)
            - **Z > 1:** Por encima del promedio (top 16%)
            - **Z = 0:** Exactamente promedio
            - **Z < -1:** Por debajo del promedio (bottom 16%)
            - **Z < -2:** Muy por debajo del promedio (bottom 2.5%)
            
            **🔸 Percentile Rankings:**
            - **99th percentile:** Elite mundial (top 1%)
            - **95th percentile:** Excelente (top 5%)
            - **75th percentile:** Bueno (top 25%)
            - **50th percentile:** Promedio
            - **25th percentile:** Por debajo del promedio
            
            **🔸 Coefficient of Variation (CV):**
            - **Qué mide:** Consistencia relativa del rendimiento
            - **CV < 0.2:** Muy consistente
            - **CV 0.2-0.5:** Moderadamente consistente
            - **CV > 0.5:** Inconsistente
            
            ### 📊 **Análisis de distribuciones:**
            
            **🔸 Histogramas con curvas de densidad:**
            - **Forma de campana:** Distribución normal (típica)
            - **Sesgo hacia la derecha:** Pocos valores muy altos
            - **Sesgo hacia la izquierda:** Pocos valores muy bajos
            - **Múltiples picos:** Diferentes poblaciones mezcladas
            
            **🔸 Box plots (Diagramas de caja):**
            - **Caja central:** 50% de los datos (Q1 a Q3)
            - **Línea central:** Mediana
            - **Whiskers:** Rango normal de datos
            - **Puntos fuera:** Outliers (valores extremos)
            
            **🔸 Q-Q plots:**
            - Compara distribución de datos con distribución teórica
            - Línea recta = distribución normal
            - Desviaciones = características especiales de los datos
            
            ### 🎮 **Métricas de eficiencia avanzadas:**
            
            **🔸 Performance per Minute (PPM):**
            - Normaliza métricas por duración de partida
            - Permite comparación entre partidas de diferentes duraciones
            - **Ejemplo:** Damage per Minute, Kills per Minute
            
            **🔸 Resource Efficiency:**
            - **Damage per Death:** Eficiencia de trading
            - **Healing per Mana:** Eficiencia de recursos
            - **Experience per Risk:** Contribution vs exposure
            
            **🔸 Relative Performance Index (RPI):**
            - Combina múltiples métricas en un solo score
            - Ponderado por importancia de cada métrica
            - Permite ranking general de rendimiento
            
            ### 📈 **Análisis predictivo:**
            
            **🔸 Correlation matrices:**
            - Muestra relaciones entre todas las métricas
            - **Correlación alta (+0.7 a +1.0):** Fuertemente relacionadas
            - **Correlación moderada (+0.3 to +0.7):** Moderadamente relacionadas
            - **Correlación baja (-0.3 to +0.3):** Poca relación
            - **Correlación negativa (-0.7 to -1.0):** Inversamente relacionadas
            
            **🔸 Regression analysis:**
            - Predice una métrica basada en otras
            - **R-squared:** Qué porcentaje de variación se explica
            - **Slope:** Qué tanto cambia Y cuando X aumenta
            - **P-value:** Qué tan significativa es la relación
            
            ### 🔄 **Análisis de clustering:**
            
            **🔸 K-means clustering:**
            - Agrupa jugadores/héroes similares automáticamente
            - Identifica archetipos naturales en los datos
            - Útil para encontrar tu "tipo" de jugador
            
            **🔸 Hierarchical clustering:**
            - Crea árbol de similitudes
            - Muestra relaciones anidadas entre grupos
            - Útil para entender spectrum de estilos de juego
            
            ### 🎯 **Métricas de impacto:**
            
            **🔸 Win Probability Added (WPA):**
            - Cuánto aumenta cada acción la probabilidad de ganar
            - Identifica jugadas más impactantes
            - Pesa acciones por contexto de la partida
            
            **🔸 Clutch Performance Index:**
            - Rendimiento en momentos críticos de la partida
            - Late game performance vs early game
            - Performance en teamfights decisivos
            
            **🔸 Meta-game Adaptation Score:**
            - Qué tan bien se adapta a cambios del meta
            - Flexibilidad en selección de héroes
            - Aprendizaje de nuevas estrategias
            
            ### 💡 **Interpretación de análisis multivariado:**
            
            **🔸 Principal Component Analysis (PCA):**
            - Reduce complejidad manteniendo información importante
            - Identifica las dimensiones más importantes del rendimiento
            - Útil para entender qué métricas realmente importan
            
            **🔸 Factor Analysis:**
            - Identifica factores subyacentes del rendimiento
            - **Ejemplo:** "Skill de combate" vs "Game sense" vs "Mecánicas"
            - Ayuda a entender diferentes tipos de habilidad
            
            ### 🔬 **Análisis de varianza (ANOVA):**
            
            **🔸 One-way ANOVA:**
            - Compara medias entre múltiples grupos
            - **Ejemplo:** ¿Difiere el rendimiento entre roles?
            - **F-statistic:** Qué tan diferentes son los grupos
            - **P-value:** Qué tan significativas son las diferencias
            
            **🔸 Two-way ANOVA:**
            - Analiza efectos de dos factores simultáneamente
            - **Ejemplo:** Efecto de rol Y mapa en rendimiento
            - Puede detectar interacciones entre factores
            
            ### 🎮 **Aplicaciones prácticas avanzadas:**
            
            **🔹 Player profiling:**
            1. Identifica tu arquetipo de jugador usando clustering
            2. Compara tu rendimiento con players similares
            3. Identifica fortalezas y debilidades específicas
            4. Establece metas realistas basadas en tu perfil
            
            **🔹 Hero optimization:**
            1. Usa PCA para entender qué hace efectivo a un héroe
            2. Identifica métricas clave para maximizar
            3. Encuentra héroes que se ajusten a tu estilo
            4. Optimiza builds basándote en análisis estadístico
            
            **🔹 Team composition science:**
            1. Usa regression para predecir éxito de composiciones
            2. Identifica sinergias no obvias con correlation analysis
            3. Optimiza draft usando análisis multivariado
            4. Predice matchups usando modelos estadísticos
            
            ### ⚠️ **Limitaciones y precauciones:**
            
            **🔸 Statistical significance:**
            - Resultados pueden ser casualidad si sample size es pequeño
            - P-hacking: encontrar patrones que no existen realmente
            - Multiple comparisons: más tests = más chance de falsos positivos
            
            **🔸 Overfitting:**
            - Modelos muy complejos pueden no generalizar
            - Validación cruzada es esencial
            - Out-of-sample testing para confirmar hallazgos
            
            **🔸 Confounding variables:**
            - Variables no medidas pueden afectar resultados
            - Correlación no implica causación
            - Context matters más que números puros
            
            **🔸 Temporal validity:**
            - Game balance changes invalidan modelos antiguos
            - Meta shifts cambian qué métricas son importantes
            - Continuous model updating es necesario
            
            ### 🏆 **Mastery objectives:**
            
            1. **Understand** distribuciones y qué formas significan
            2. **Interpret** correlaciones y su significado práctico
            3. **Apply** clustering para encontrar tu arquetipo
            4. **Use** predictive models para optimizar decisiones
            5. **Validate** hallazgos con out-of-sample testing
            6. **Adapt** análisis cuando el meta cambie
            """
        }
    }
    
    if section_type in explanations:
        with st.expander(explanations[section_type]['title'], expanded=False):
            st.markdown(explanations[section_type]['content'])
    else:
        with st.expander("📖 Información sobre esta sección", expanded=False):
            st.info("Explicación detallada no disponible para esta sección.")


def create_general_explanation():
    """
    Crea una explicación general sobre cómo usar el dashboard
    """
    with st.expander("🎮 ¿Cómo usar este Dashboard? - Guía para principiantes", expanded=False):
        st.markdown("""
        ### 🎯 **¿Qué es este Dashboard?**
        
        Este es un dashboard de análisis para Heroes of the Storm que te ayuda a entender:
        - **Rendimiento de jugadores** y héroes
        - **Tendencias** en el tiempo
        - **Estrategias** efectivas
        - **Métricas** importantes del juego
        
        ### 🧭 **Navegación básica:**
        
        **🔸 Barra lateral izquierda:**
        - **Configuración:** Selecciona el dataset (temporada/período)
        - **Secciones:** Elige qué tipo de análisis ver
        - **Filtros:** Personaliza qué datos mostrar
        
        **🔸 Área principal:**
        - **Gráficos interactivos:** Haz click para ver detalles
        - **Tablas:** Ordena por columnas haciendo click en headers
        - **Métricas:** Valores clave destacados en tarjetas
        
        ### 📊 **Tipos de análisis disponibles:**
        
        1. **📊 Análisis General:** Rendimiento de héroes y métricas básicas
        2. **🏆 Rankings de Players:** Los mejores jugadores en diferentes métricas
        3. **🦸‍♂️ Rankings de Héroes:** Los héroes más efectivos
        4. **📈 Tendencias:** Evolución de métricas en el tiempo
        5. **🚀 Analytics Profesional:** Análisis avanzados tipo pro-play
        6. **🔍 Exploración de Datos:** Herramientas para investigar libremente
        7. **📋 Análisis de Composiciones:** Combinaciones de héroes efectivas
        8. **🎯 Métricas Avanzadas:** Estadísticas complejas y predictivas
        
        ### 🎮 **Métricas importantes explicadas:**
        
        **💀 Combate:**
        - **HeroKills:** Héroes enemigos eliminados (más = mejor)
        - **Deaths:** Veces que moriste (menos = mejor)
        - **Assists:** Ayudaste en eliminaciones (más = mejor teamwork)
        
        **⚔️ Daño:**
        - **HeroDamage:** Daño a héroes enemigos (más = mayor impacto)
        - **SiegeDamage:** Daño a estructuras (más = mejor push)
        - **Healing:** Curación a aliados (más = mejor support)
        
        **🏆 Rendimiento:**
        - **KDA Ratio:** (Kills + Assists) / Deaths (>1.5 es bueno)
        - **Win Rate:** Porcentaje de victorias
        - **Experience:** Contribución de XP al equipo
        
        ### 💡 **Consejos para principiantes:**
        
        1. **Empieza simple:** Ve primero "Análisis General" y "Rankings"
        2. **Usa filtros:** Selecciona tu héroe favorito para ver solo esos datos
        3. **Compara:** Ve cómo te comparas con los mejores jugadores
        4. **Busca patrones:** ¿Qué héroes/estrategias funcionan mejor?
        5. **Lee las explicaciones:** Cada sección tiene explicaciones detalladas al final
        
        ### ❓ **¿Necesitas ayuda?**
        
        - **Cada sección** tiene una guía detallada al final
        - **Hover** sobre gráficos para ver información adicional
        - **Click** en elementos interactivos para explorar más
        - Los **colores** y **tamaños** en gráficos tienen significado específico
        
        ¡Disfruta explorando tus datos de Heroes of the Storm! 🎮
        """)
