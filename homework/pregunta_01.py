# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    df = load_data("files\input\shipping-data.csv")

    create_visual_for_shipping_per_warehouse(df)
    create_visual_for_mode_of_shipment(df)
    create_visual_for_average_customer_rating(df)
    create_visual_for_weight_distribution(df)
    create_dashboard()


def load_data(input_file):
    df = pd.read_csv(input_file)
    return df


def save_file(name, output_directory="docs"):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    plt.savefig(f"{output_directory}/{name}.png")


def create_visual_for_shipping_per_warehouse(df):
    df = df.copy()
    plt.figure()

    counts = df.Warehouse_block.value_counts()
    counts.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record Count",
        color="tab:blue",
        fontsize=8,
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    save_file("shipping_per_warehouse")


def create_visual_for_mode_of_shipment(df):
    df = df.copy()
    plt.figure()
    counts = df.Mode_of_Shipment.value_counts()
    counts.plot.pie(
        title="Model of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors={"tab:blue", "tab:orange", "tab:green"},
    )
    save_file("mode_of_shipment")


def create_visual_for_average_customer_rating(df):
    df = df.copy()
    plt.figure()
    df = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    df.columns = df.columns.droplevel()
    df = df[["mean", "min", "max"]]
    plt.barh(
        y=df.index.values,
        width=df["max"].values - 1,
        left=df["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df["mean"].values
    ]

    plt.barh(
        y=df.index.values,
        width=df["mean"].values - 1,
        left=df["min"].values,
        height=0.5,
        color=colors,
        alpha=1,
    )

    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    save_file("average_customer_rating")


def create_visual_for_weight_distribution(df):
    df = df.copy()
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title="Shipped Weight Distribution", color="tab:orange", edgecolor="white"
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    save_file("weight_distribution")


def create_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Shipping Dashboard Example</h1>
        <div style="width:45%;float:left">
            <img src="../docs/shipping_per_warehouse.png" alt="Fig 1">
            <img src="../docs/mode_of_shipment.png" alt="Fig 2">
        </div>
        <div style="width:45%;float:left">
            <img src="../docs/average_customer_rating.png" alt="Fig 3">
            <img src="../docs/weight_distribution.png" alt="Fig 4">
        </div>
    </body>
    </html>
    """

    # Crear el archivo HTML
    with open("docs/index.html", "w") as archivo:
        archivo.write(html_content)


if "__main__" in __name__:
    pregunta_01()
