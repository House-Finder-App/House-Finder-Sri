declare module 'opencv4nodejs' {
  export class Mat {
    cvtColor(code: number): Mat;
    gaussianBlur(size: Size, sigma: number): Mat;
    getDataAsArray(): number[][][];
    copy(): Mat;
    drawRectangle(rect: Rect, color: Vec3, thickness: number): void;
    release(): void;
  }

  export class Size {
    constructor(width: number, height: number);
    width: number;
    height: number;
  }

  export class Rect {
    constructor(x: number, y: number, width: number, height: number);
    x: number;
    y: number;
    width: number;
    height: number;
  }

  export class Vec3 {
    constructor(x: number, y: number, z: number);
  }

  export class CascadeClassifier {
    constructor(path: string);
    detectMultiScale(
      image: Mat,
      options: {
        scaleFactor?: number;
        minNeighbors?: number;
        minSize?: Size;
        maxSize?: Size;
      }
    ): Rect[];
  }

  export function imread(path: string): Mat;
  export function imwrite(path: string, image: Mat): void;

  export const COLOR_BGR2GRAY: number;
} 