const express = require('express');
const cors = require('cors');
const nodemailer = require('nodemailer');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Хранилище кодов в памяти (для тестов)
const verificationCodes = {};

// Настройка отправителя писем (SMTP)
const transporter = nodemailer.createTransport({
    service: 'gmail', // Можно использовать Yandex, Mail.ru и др.
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS  // Пароль приложения
    }
});

// 1. Ручка генерации и отправки кода
app.post('/api/send-code', async (req, res) => {
    const { email } = req.body;
    if (!email) return res.status(400).json({ error: 'Email обязателен' });

    // Генерация 6-значного кода
    const code = Math.floor(100000 + Math.random() * 900000).toString();
    verificationCodes[email] = code;

    try {
        await transporter.sendMail({
            from: `"Auth System" <${process.env.EMAIL_USER}>`,
            to: email,
            subject: 'Ваш код подтверждения',
            text: `Ваш код для регистрации: ${code}`
        });
        res.json({ success: true, message: 'Код отправлен на почту' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Ошибка отправки письма' });
    }
});

// 2. Ручка проверки кода
app.post('/api/verify-code', (req, res) => {
    const { email, code } = req.body;
    if (verificationCodes[email] && verificationCodes[email] === code) {
        delete verificationCodes[email]; // Удаляем использованный код
        return res.json({ success: true, message: 'Код верен!' });
    }
    res.status(400).json({ error: 'Неверный код или email' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
