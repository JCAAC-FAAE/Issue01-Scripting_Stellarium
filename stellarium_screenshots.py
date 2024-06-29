from pathlib import Path
from textwrap import dedent


def stellarium_screenshots(path, script_name, object_name, jds, fov_deg, label_fmt={}):
    """
    Genera un script para Stellarium que permite visualizar
    fenómenos mediante una secuencia de capturas de pantallas
    correspondientes a la lista de fechas julianas dada.
    Stellarium guarda las capturas de pantalla en su directorio
    por defecto (Windows: Imágenes\Stellarium, MacOS: escritorio,
    Linux: home), usando nombres de fichero según la plantilla:
    '{script_name}_NNN.png'.

    Parámetros
    ----------
    script_name : str
        nombre del fichero para el script, sin extensión (se
        añade ".ssc" automáticamente)
    object_name : str
        nombre del objeto a buscar
    jds : iterable
        lista de fechas julianas (UTC) para cada captura de
        pantalla
    fov_deg : float
        FOV (grados)
    label_fmt : dict
        diccionario con las propiedades para la etiqueta que
        muestra la fecha y hora. Es opcional, se proporcionan
        valores por defecto si se omite. Las claves son:
          'size': tamaño de la fuente en píxeles;
          'color': especificado en notación HTML, p.ej. '#ffffff'
          'side': orientación respecto del objeto, 'N', 'S', 'E', 'W'
          'distance': distancia en píxeles respecto del centro del
          objeto.
    """

    # Plantilla para script de secuencia de capturas de pantalla
    # En Los bloques de código javascript delimitados por llaves,
    # hay que sustituirlas por dobles llaves: { --> {{, } -> }}.
    # Esto es necesario para evitar confusiones en la sustitución
    # realizada por str.format().
    stel_screenshots_tpl = """
    /*
    * Configuración
    */

    var lbl = LabelMgr.labelObject(
        '',
        '{object_name}',
        true,
        {size}, '{color}',
        '{side}', {distance}
    );

    core.setGuiVisible(false);
    core.setMountMode('equatorial');
    core.setTimeRate(0.0);
    core.selectObjectByName('{object_name}');
    core.setSelectedObjectInfo('None');
    LandscapeMgr.setFlagLandscape(false);
    StelMovementMgr.setAutoMoveDuration(0.0);
    StelMovementMgr.setFlagTracking(true);
    StelMovementMgr.zoomTo({fov_deg}, 0.0);
    SolarSystem.setFlagPointer(false);
    SolarSystem.setFlagOrbits(false);

    /*
    * Bucle principal
    */

    var jd = [
      {jd_list}
    ];

    function getDateHM() {{
    return core
      .getDate('local')
      .replace('T', ' ')
      .slice(0, -3);
    }}

    function display_event(i) {{
      core.setJDay(jd[i]);
      LabelMgr.setLabelText(lbl, getDateHM());
      core.wait(0.1);
    }}

    const prefix = '{script_name}_';
    for (var i = 0; i < jd.length; i++) {{
      display_event(i);
      core.screenshot(prefix);
    }}

    /*
    * Limpieza
    */
    LabelMgr.deleteAllLabels();
    core.setGuiVisible(true);
    """

    # Valores por defecto para formato de la etiqueta de fecha/hora
    def_label_fmt = {"size": 36, "color": "#ffffff", "side": "N", "distance": 250}

    # Preparación del diccionario para sustitución de valores
    script_fname = f"{script_name}.ssc"
    jd_list = [str(jd) for jd in jds]
    mapping = (
        def_label_fmt
        | label_fmt
        | {
            "script_name": script_name,
            "jd_list": ",\n  ".join(jd_list),
            "object_name": object_name,
            "fov_deg": round(fov_deg, 4),
        }
    )

    # Sustitución de valores sobre la plantilla (tras "des-indentarla")
    script = dedent(stel_screenshots_tpl).format(**mapping)

    # Salvar script resultante a fichero de texto
    with open(Path(path) / script_fname, "w", encoding="utf-8") as f:
        f.writelines(script)


# __/ Ejemplo de uso: fenómenos triples galileanos \__________
jds = [
    2460967.0585855003,
    2461386.423732,
    2463312.0232595,
    2463362.3377175,
    2463462.443047,
    2463596.925324,
    2465306.6901634997,
    2465340.340205,
    2465490.652805,
    2465641.2397775,
    2465775.727678,
    2467517.125278,
    2467986.2149755,
    2468171.1002674997,
    2468271.1420334997,
]
fov_deg = 1 / 60  # 1 arcmin

# Genera el fichero triple_galilean.ssc en el directorio actual
stellarium_screenshots(".", "triple_galilean", "Jupiter", jds, fov_deg)
