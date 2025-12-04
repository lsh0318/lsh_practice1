import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# 数据
file_path = "C:/Users/15354/PyCharmMiscProject/392程序设计实战考试/corpus.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\n', ' <<eos>> ')  # 句子分隔符
tokens = text.split()

tokenizer = Tokenizer(filters='', oov_token='<unk>')
tokenizer.fit_on_texts([tokens])
vocab_size = len(tokenizer.word_index) + 1

print(f"词汇表大小: {vocab_size}")

int_sequence = tokenizer.texts_to_sequences([tokens])[0]

def create_sequences(sequence, seq_length=3):
    X, y = [], []
    for i in range(len(sequence) - seq_length):
        X.append(sequence[i:i + seq_length])
        y.append(sequence[i + seq_length])
    return np.array(X), np.array(y)

size = 3
X, y = create_sequences(int_sequence, size)

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.1, random_state=42, shuffle=True
)

y_train_onehot = to_categorical(y_train, num_classes=vocab_size)
y_val_onehot = to_categorical(y_val, num_classes=vocab_size)

#构建
embedding_dim = 32
lstm_units = 64

model = Sequential([
    Embedding(
        input_dim=vocab_size,
        output_dim=embedding_dim,
        input_length=size,
        mask_zero=False
    ),
    Bidirectional(LSTM(lstm_units, return_sequences=False)),
    Dropout(0.3),
    Dense(lstm_units, activation='relu'),
    Dropout(0.2),
    Dense(vocab_size, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()

#训练
epochs = 100
batch_size = 16

history = model.fit(
    X_train, y_train_onehot,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(X_val, y_val_onehot),
    shuffle=True
)

#预测
def generate_text(model, tokenizer, seed_text, max_length=20):
    for _ in range(max_length):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]

        if len(token_list) > size:
            token_list = token_list[-size:]
        elif len(token_list) < size:
            token_list = [0] * (size - len(token_list)) + token_list

        predicted_probs = model.predict(np.array([token_list]), verbose=0)[0]
        predicted_id = np.argmax(predicted_probs)

        output_word = tokenizer.index_word.get(predicted_id, '<unk>')
        seed_text += " " + output_word

        if output_word == '<<eos>>' or output_word == '<end>':
            break

    return seed_text
