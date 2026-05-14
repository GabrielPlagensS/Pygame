def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("v "):
                _, x, y, z = line.strip().split()
                vertices.append([float(x), float(y), float(z)])

            elif line.startswith("f "):
                parts = line.strip().split()[1:]
                face = []

                for part in parts:
                    # Suporta formatos como 1, 1/2/3, 1//3
                    index = int(part.split("/")[0]) - 1
                    face.append(index)

                faces.append(face)

    return vertices, faces