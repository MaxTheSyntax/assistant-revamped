import customtkinter as ctk
import completion, var
import logging as l

## General styles
frame_padding = 10
button_padding = 5

def init():
    global messages_frame, info_frame

    root = ctk.CTk()

    ## Window
    root.geometry("900x400")
    root.title("Assistant Revamped")

    ## Appearance
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    ## Configure grid layout
    root.grid_columnconfigure(0, weight=4)  # Messages column
    root.grid_columnconfigure(1, weight=2)  # Info column
    root.grid_rowconfigure(0, weight=1)     # Main content row
    root.grid_rowconfigure(1, weight=0)     # Action row

    ## Messages frame
    messages_frame = ctk.CTkScrollableFrame(root, label_text="Messages")
    messages_frame.grid(row=0, column=0, sticky="nsew", padx=frame_padding, pady=frame_padding)

    ## Info frame
    info_frame = ctk.CTkScrollableFrame(root, label_text="Last message")
    info_frame.grid(row=0, column=1, sticky="nsew", padx=frame_padding, pady=frame_padding)

    ## Action frame
    action_frame = ctk.CTkFrame(root)
    action_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=frame_padding, pady=frame_padding)

    ## Text input button
    text_input_button = ctk.CTkButton(action_frame, text="Open Text Input", command=open_text_input)
    text_input_button.pack(side="left", expand=True, pady=button_padding)

    settings_button = ctk.CTkButton(action_frame, text="Open Settings")
    settings_button.pack(side="left", expand=True, pady=button_padding)

    ## JSON button
    json_button = ctk.CTkButton(action_frame, text="Open JSON response")
    json_button.pack(side="left", expand=True, pady=button_padding)

    ## Quit button
    quit_button = ctk.CTkButton(action_frame, text="Quit")
    quit_button.pack(side="left", expand=True, pady=button_padding)

    ## Start GUI loop
    update_messages()
    root.update()
    root.mainloop()

def open_text_input():
    input_window = ctk.CTkToplevel()
    input_window.title("Text Input")
    input_window.geometry("400x300")

    text_input = ctk.CTkTextbox(input_window)
    text_input.pack(fill="both", expand=True, padx=frame_padding, pady=frame_padding)

    def send():
        completion.reply(text_input.get("1.0", "end-1c"))
        text_input.delete("1.0", "end")

    send_button = ctk.CTkButton(input_window, text="Send", command=send)
    send_button.pack(pady=10)

last_message = 0
def update_messages():
    global last_message
    l.debug(f"Updating messages from {last_message}...")
    if last_message < len(var.messages):
        ## Update messages frame
        for msg in var.messages[last_message:]:
            # Get role and content depending on message structure
            if isinstance(msg, dict):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
            else:
                # We assume it's a ChatCompletionMessage object
                role = msg.role
                content = msg.content

            text_alignment = "e" if role == "user" else "w"
            icon = "👤" if role == "user" else "✨"
            msg_label = ctk.CTkLabel(messages_frame, text=f" {icon} {role.capitalize()}: {content}", wraplength=400, justify="left", anchor=text_alignment)
            msg_label.pack(fill="x", padx=5, pady=5)

        # Update info frame with the last message
        # last_msg = var.messages[-1]
        # info_label = ctk.CTkLabel(info_frame, text=f"Role: {last_msg['role']}\nContent: {last_msg['content']}", wraplength=200, justify="left", anchor="w")
        # info_label.pack(fill="x", padx=5, pady=5)

        last_message = len(var.messages)
        l.debug(f"Updated messages to {last_message} entries.")
    