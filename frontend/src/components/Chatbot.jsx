import { useState } from "react";
import axios from "axios";
import { PaperAirplaneIcon } from "@heroicons/react/24/solid";


const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", { message: input });
      const botMessage = { sender: "bot", text: response.data.reply };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error:", error);
    }

    setInput("");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-lg bg-white shadow-lg rounded-xl p-4">
        <h1 className="text-xl font-semibold text-gray-700 text-center">🗣️ குறலி - Tamil Chatbot</h1>

        <div className="h-96 overflow-y-auto p-2 border my-4 rounded bg-gray-50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`my-2 p-2 rounded-lg ${msg.sender === "user" ? "bg-blue-100 text-right" : "bg-green-100 text-left"}`}
            >
              <strong>{msg.sender === "user" ? "You" : "குறலி"}:</strong> {msg.text}
            </div>
          ))}
        </div>

        <div className="flex items-center border rounded-lg p-2">
          <input
            type="text"
            className="flex-1 p-2 outline-none"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage} className="bg-blue-500 text-white p-2 rounded-lg">
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
