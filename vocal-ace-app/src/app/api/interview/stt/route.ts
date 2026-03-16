import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ error: 'No audio file provided' }, { status: 400 });
    }

    // Proxy to local Python STT service
    const localSttUrl = process.env.LOCAL_STT_URL || 'http://localhost:8001/transcribe';

    const backendFormData = new FormData();
    backendFormData.append('file', file);

    const response = await axios.post(localSttUrl, backendFormData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return NextResponse.json({ text: response.data.text });
  } catch (error: any) {
    console.error('Local STT error:', error.message);
    return NextResponse.json({ error: 'Failed to transcribe audio locally. Ensure the Python STT service is running on port 8001.' }, { status: 500 });
  }
}
