import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { EventEmitter2, EventEmitterModule } from '@nestjs/event-emitter';
import { ClientsModule, Transport } from '@nestjs/microservices';

@Module({
  imports: [
    EventEmitterModule,
    ClientsModule.register([
      {
        name: 'REDIS',
        transport: Transport.REDIS,
        options: {
          host: '127.0.0.1',
          port: 6379,
          retryAttempts: 99999999999,
          retryDelay: 3000,
        },
      },
    ]),
  ],
  controllers: [AppController],
  providers: [AppService, EventEmitter2],
})
export class AppModule { }
