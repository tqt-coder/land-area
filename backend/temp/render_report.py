import numpy as np
import matplotlib.pyplot as plt

def visualize_mask(mask):
    plt.pcolormesh(mask, cmap="binary")  # Reshape for plotting
    # Optional: Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("2D Array Visualization")
    plt.savefig("my_mask_visualization.png")

def calculate_area(image, mask):
	unique_values, counts = np.unique(image[mask], return_counts=True)

	area={}
	for i in range(len(unique_values)):
		area[unique_values[i]] = counts[i]*0.3*0.3
	print(area)

#edit here
#split the big mask to 64 small ones
#mask size depend on the image on dataset
#link dataset: https://drive.google.com/drive/folders/1HUd84yzf88tOZmYqmIrJKK7QrD2dwGMx
def split_mask(image, mask):
	pass

def main():
	# mask = np.load(s'mask.npy')
	#visualize_mask(mask)
	# split_mask(mask)
	image = np.array([[1, 2, 1], [1, 3, 2], [3, 1, 2]])
	mask = np.array([[True, False, True], [True, True, False], [False, True, False]])
	calculate_area(image,mask)

if __name__ == '__main__':
	main()
