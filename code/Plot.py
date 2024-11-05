import matplotlib.pyplot as plt


def plot_results(results):
    x_values = [d["x"] for d in results]
    y_values = [d["y"] for d in results]
    z_values = [d["z"] for d in results]
    result_values = [d["result"] for d in results]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x_values, y_values, z_values, c=result_values, marker="o")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("EMFI Scan Result")
    plt.show()
