import { NextRequest, NextResponse } from 'next/server';
import pdf from 'pdf-parse';

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as Blob;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    const buffer = Buffer.from(await file.arrayBuffer());
    const data = await pdf(buffer);

    return NextResponse.json({
      text: data.text,
      info: data.info,
      metadata: data.metadata,
      pages: data.numpages
    });
  } catch (error: any) {
    console.error('Resume parsing error:', error);
    return NextResponse.json({ error: 'Failed to parse PDF resume' }, { status: 500 });
  }
}
