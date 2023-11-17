import { Controller, Sse } from '@nestjs/common';
import { Observable } from 'rxjs';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { MessagePattern, Payload } from '@nestjs/microservices';

@Controller()
export class AppController {
  private readonly eventStream: Observable<MessageEvent>;

  constructor(private readonly eventEmitter: EventEmitter2) {
    this.eventStream = new Observable<MessageEvent>((eventSubscriber) => {
      this.eventEmitter.on('ALERT', (data) => {
        eventSubscriber.next({
          data: data,
        } as MessageEvent);
      });
      this.eventEmitter.on('CLOSE', () => {
        eventSubscriber.complete();
      });
    });
  }

  @MessagePattern('workers:events')
  async handleWorkerEvents(@Payload() data: any) {
    console.log(data);
    this.eventEmitter.emit('ALERT', data);
  }

  @Sse('workers/events')
  eventStreamer(): Observable<MessageEvent> {
    return this.eventStream;
  }
}
