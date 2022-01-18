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


# If watermark's size has y > x, scale its x to 10% of the image's x. Then scale y to keep same ratio.
# If watermark's size has x > y, scale its y to 10% of the image's y. Then scale x to keep same ratio.
def watermark_resize():
    if image_hub["mark"].size[1] > image_hub["mark"].size[0]:
        new_x = int(0.1 * image_hub["img"].size[0])
        scale_ratio = new_x / image_hub["mark"].size[0]
        new_y = int(image_hub["mark"].size[1] * scale_ratio)
        image_hub["mark"] = image_hub["mark"].resize((new_x, new_y))
    else:
        new_y = int(0.1 * image_hub["img"].size[1])
        scale_ratio = new_y / image_hub["mark"].size[1]
        new_x = int(image_hub["mark"].size[0] * scale_ratio)
        image_hub["mark"] = image_hub["mark"].resize((new_x, new_y))


# Scale then paste watermark over image and save result. Create ImageTk to update the image preview label.
def update_image(anchor=(0, 0)):
    # Have to catch KeyError as this can be called before both images have been uploaded.
    try:
        watermark_resize()
        combined_img = image_hub["img"].copy()
        # Try to use watermark as mask to apply transparency. Catch error and remove mask if no transparency.
        try:
            combined_img.paste(image_hub["mark"], box=anchor, mask=image_hub["mark"])
        except ValueError:
            combined_img.paste(image_hub["mark"], box=anchor)

        img_tk = ImageTk.PhotoImage(combined_img)
        current_image.configure(image=img_tk)
        current_image.image = img_tk

        combined_img.save("marked images/combined.jpg", "JPEG")
    except KeyError:
        pass


def watermark_move(event):
    update_image((event.x, event.y))


# Used to store Image objects for image upload, watermark upload, and current blend of the two.
image_hub = {}

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

# Buttons + Path labels are their own frame with a 2x2 grid.
button_frame = ttk.Frame(frame, padding=10)
button_frame.grid(column=0, row=2, sticky="nswe")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=2)

ttk.Button(button_frame, text="Upload Image", command=image_upload).grid(column=0, row=0, sticky="ew")
watermark_button = ttk.Button(button_frame, text="Upload Watermark", command=watermark_upload)
watermark_button.grid(column=0, row=1, sticky="ew")

image_path = ttk.Label(button_frame, text="Current Image: NONE", background="white")
image_path.grid(column=1, row=0, sticky="ew")
watermark_path = ttk.Label(button_frame, text="Current Watermark: NONE", background="white")
watermark_path.grid(column=1, row=1, sticky="ew")

root.mainloop()
