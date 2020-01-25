import { Subscription } from 'rxjs';

export interface WebSocketCallback {
    page: string;
    eventName: string;
    callback: (data: any) => void;
    subscription: Subscription;
}
