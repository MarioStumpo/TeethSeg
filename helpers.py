import os
import numpy as np
from scipy.spatial import distance

def get_barycenters_by_label(mesh, labels):
    """
    Calculate the barycenters for each unique label in the mesh.
    """
    label_barycenters = {}
    for label in np.unique(labels):
        label_cells = labels == label
        barycenters = mesh.cell_centers()[label_cells]
        label_barycenters[label] = barycenters.mean(axis=0)
    return label_barycenters

def is_adjacent(mesh, label_1, label_2):
    """
    Check if two labels are adjacent by examining shared vertices or faces.
    """
    label_1_cells = np.where(mesh.celldata['Label'] == label_1)[0]
    label_2_cells = np.where(mesh.celldata['Label'] == label_2)[0]
    for cell_1 in label_1_cells:
        for cell_2 in label_2_cells:
            shared_points = np.intersect1d(mesh.faces()[cell_1], mesh.faces()[cell_2])
            if len(shared_points) >= 2:  # Shared edge
                return True
    return False

def calculate_distances(mesh):
    """
    Calculate distances between adjacent labels in the segmented mesh.
    """
    labels = mesh.celldata['Label']
    label_barycenters = get_barycenters_by_label(mesh, labels)

    distances = {}
    for label, center in label_barycenters.items():
        distances[label] = {"adjacent_labels": [], "distances": []}
        for other_label, other_center in label_barycenters.items():
            if label != other_label and is_adjacent(mesh, label, other_label):
                dist = np.linalg.norm(center - other_center)
                distances[label]["adjacent_labels"].append(other_label)
                distances[label]["distances"].append(dist)
    return distances

def delete_temp_file(folder_path, filename):
    file_path = os.path.join(folder_path, filename + ".vtp")
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

def delete_temp_files(folder_path):
    """
    Delete all files in the specified folder.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def create_temp_file(folder_path, filename, binary_data):
    temp_filepath = os.path.join(folder_path, filename)
    with open(temp_filepath, "wb") as temp_file:
        temp_file.write(binary_data)
    return temp_filepath
