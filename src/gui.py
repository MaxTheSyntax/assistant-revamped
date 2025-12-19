import customtkinter as ctk
import completion
import common as c
import logging as l

## General styles
frame_padding = 10
button_padding = 5
label_padding = 5

def init():
    """Initializes the GUI application. Runs the main loop."""

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

    ## Action frame elements

    ## Text input button
    text_input_button = ctk.CTkButton(action_frame, text="Open Text Input", command=open_text_input)
    text_input_button.pack(side="left", expand=True, pady=button_padding)

    ## Settings button
    settings_button = ctk.CTkButton(action_frame, text="Open Settings")
    settings_button.pack(side="left", expand=True, pady=button_padding)

    ## JSON button
    json_button = ctk.CTkButton(action_frame, text="Open JSON response")
    json_button.pack(side="left", expand=True, pady=button_padding)

    ## Quit button
    quit_button = ctk.CTkButton(action_frame, text="Quit")
    quit_button.pack(side="left", expand=True, pady=button_padding)

    ## Info frame elements

    ## Waiting label
    waiting_label = ctk.CTkLabel(info_frame, text="Waiting for messages...", wraplength=200, justify="left", anchor="w")
    waiting_label.pack(fill="x", padx=5, pady=5)

    ## Start GUI loop
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
    """
    Updates the messages displayed in the GUI and refreshes the information frame 
    with details about the last message.
    """
    global last_message
    l.debug(f"Updating messages from {last_message}...")

    def get_role_and_content(msg):
        """
        Extracts the role and content from a message object.

        Args:
            msg (Union[dict, object]): The message object, which can either be a dictionary
                or an object with 'role' and 'content' attributes.

        Returns:
            tuple: A tuple containing the role (str) and content (str) of the message.
                If the message is a dictionary, the 'role' key defaults to "unknown" 
                and the 'content' key defaults to an empty string if not present.
        """
        if isinstance(msg, dict):
            return msg.get("role", "unknown"), msg.get("content", "")
        else:
            return msg.role, msg.content

    if last_message < len(c.chat):
        ## Update messages frame
        for msg in c.chat[last_message:]:
            role, content = get_role_and_content(msg)

            text_alignment = "e" if role == "user" else "w"
            icon = "👤" if role == "user" else "✨"
            msg_label = ctk.CTkLabel(messages_frame, text=f" {icon} {role.capitalize()}: {content}", wraplength=400, justify="left", anchor=text_alignment)
            msg_label.pack(fill="x", padx=5, pady=5)

        ## Update info frame with the last message
        if len(c.chat) < 2:
            return  # Not enough messages to display info
        last_msg = c.chat[-1] if get_role_and_content(c.chat[-1])[0] != "system" else c.chat[-2]
        role, content = get_role_and_content(last_msg)

        ## Info frame elements

        ## Delete old labels
        for widget in info_frame.winfo_children():
            widget.destroy()

        lc = getattr(last_msg, 'logit_config', None)

        ## Model label
        model_label = ctk.CTkLabel(info_frame, text=f"Model: {getattr(lc, 'model', 'N/A')}", wraplength=200, justify="left", anchor="w")
        model_label.pack(fill="x", padx=label_padding, pady=label_padding)

        ## Provider label
        provider_label = ctk.CTkLabel(info_frame, text=f"Provider: {getattr(lc, 'provider', 'N/A')}", wraplength=200, justify="left", anchor="w")
        provider_label.pack(fill="x", padx=label_padding, pady=label_padding)

        ## Cost label
        cost_label = ctk.CTkLabel(info_frame, text=f"Cost: {getattr(lc, 'cost', 'N/A')}", wraplength=200, justify="left", anchor="w")
        cost_label.pack(fill="x", padx=label_padding, pady=label_padding)

        ## BYOK label
        byok_label = ctk.CTkLabel(info_frame, text=f"Is BYOK: {getattr(lc, 'is_byok', 'N/A')}", wraplength=200, justify="left", anchor="w")
        byok_label.pack(fill="x", padx=label_padding, pady=label_padding)
        
        last_message = len(c.chat)
        l.debug(f"Updated messages to {last_message} entries.")
    