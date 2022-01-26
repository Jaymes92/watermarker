from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


# Save PIL Image of selected image to image_hub. Update image path label and image preview.
def image_upload():
    filename = filedialog.askopenfilename(title="Select an image!",
                                          initialdir=".",
                                          filetypes=[("Pics", ".jpg .jpeg .png .gif")])
    img = Image.open(filename)
    image_hub["img"] = img
    image_path.configure(text=filename)
    update_image()


# Save PIL Image of selected water to image_hub. Update watermark path label and image preview.
def watermark_upload():
    filename = filedialog.askopenfilename(title="Select an image!",
                                          initialdir=".",
                                          filetypes=[("Pics", ".jpg .jpeg .png .gif")])
    mark = Image.open(filename)
    image_hub["mark"] = mark
    watermark_path.configure(text=filename)
    update_image()


# Scale then paste watermark over image and save result. Create ImageTk to update the image preview label.
def update_image():
    # Catch KeyError as this can be called before both images have been uploaded.
    try:
        combined_img = image_hub["img"].copy()
        # If watermark's size has y < x, scale its x to input multiple of image. Then scale y to keep same ratio.
        # If watermark's size has x < y, scale its y to input multiple of image. Then scale x to keep same ratio.
        if image_hub["mark"].size[1] < image_hub["mark"].size[0]:
            new_x = int(scale_var.get() * image_hub["img"].size[0])
            scale_ratio = new_x / image_hub["mark"].size[0]
            new_y = int(image_hub["mark"].size[1] * scale_ratio)
            scaled_mark = image_hub["mark"].resize((new_x, new_y))
        else:
            new_y = int(scale_var.get() * image_hub["img"].size[1])
            scale_ratio = new_y / image_hub["mark"].size[1]
            new_x = int(image_hub["mark"].size[0] * scale_ratio)
            scaled_mark = image_hub["mark"].resize((new_x, new_y))
        # Try to use watermark as mask to apply transparency. Catch error and use no mask if no transparency.
        try:
            combined_img.paste(scaled_mark, box=image_hub["anchor"], mask=scaled_mark)
        except ValueError:
            combined_img.paste(scaled_mark, box=image_hub["anchor"])
        # Just used to update GUI
        img_tk = ImageTk.PhotoImage(combined_img)
        current_image.configure(image=img_tk)
        current_image.image = img_tk

        combined_img.save("marked images/combined.png", "PNG")
    except KeyError:
        pass


def watermark_move(event):
    image_hub["anchor"] = (event.x, event.y)
    update_image()


def scale_update(event):
    scale_var.set(event)
    update_image()


# Used to store Image objects for image upload, watermark upload, and current anchor.
image_hub = {"anchor": (0, 0)}

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("Watermark Designer")

# Base frame which contains all the other components.
frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0, sticky="nswe")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

ttk.Label(frame, text="Watermark Maker", anchor=CENTER).grid(column=0, row=0, sticky="ew")

current_image = ttk.Label(frame, anchor=CENTER)
current_image.grid(column=0, row=1, sticky="nsew")
current_image.bind("<Button-1>", watermark_move)
current_image.bind("<B1-Motion>", watermark_move)

# Sub frame to contain upload buttons + labels and scale widget + label.
button_frame = ttk.Frame(frame, padding=10)
button_frame.grid(column=0, row=2, sticky="nswe")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=2)

image_button = ttk.Button(button_frame, text="Upload Image", command=image_upload)
image_button.grid(column=0, row=0, sticky="ew")
watermark_button = ttk.Button(button_frame, text="Upload Watermark", command=watermark_upload)
watermark_button.grid(column=0, row=1, sticky="ew")

image_path = ttk.Label(button_frame, text="Current Image: NONE", background="white")
image_path.grid(column=1, row=0, sticky="ew")
watermark_path = ttk.Label(button_frame, text="Current Watermark: NONE", background="white")
watermark_path.grid(column=1, row=1, sticky="ew")

scale_label = ttk.Label(button_frame, text="Watermark Scale (%): ")
scale_label.grid(column=0, row=2, sticky="e")

scale_var = DoubleVar()
scale = ttk.Scale(button_frame, from_=0.01, to=0.9, length=300, variable=scale_var, command=scale_update)
scale_var.set(0.3)
scale.grid(column=1, row=2, sticky="w")

root.mainloop()
