export default async function handler(req, res) {
    // Разрешаем кросс-доменные запросы (CORS)
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') return res.status(200).end();
    if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' });

    // ТОКЕН ВАШЕГО БОТА
    const BOT_TOKEN = "8872260684:AAHU65LnhHmLAItW3J6ECA-l9RyAOaSwAy8";
    const { stars = 5 } = req.body || {};

    try {
        const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/createInvoiceLink`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: "Попытка в рулетке",
                description: `Вращение рулетки за ${stars} звезд`,
                payload: `spin_${stars}_stars`,
                provider_token: "", // Для Telegram Stars оставляем пустым
                currency: "XTR",   // Код валюты Telegram Stars
                prices: [{ label: "Звезды", amount: Number(stars) }]
            })
        });

        const data = await response.json();

        if (data.ok) {
            // Возвращаем готовую ссылку t.me/$...
            return res.status(200).json({ invoice_url: data.result });
        } else {
            return res.status(400).json({ error: data.description || 'Ошибка Telegram API' });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}
