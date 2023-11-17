import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.REDIS,
    options: {
      retryDelay: 5000,
      retryAttempts: 10000,
      host: '127.0.0.1',
      port: 6379,
    },
  });

  await app.startAllMicroservices();
  await app.listen(8001);
}
bootstrap();
