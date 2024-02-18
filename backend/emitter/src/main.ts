import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const configService = app.get(ConfigService);
  const PORT = configService.get('PORT');
  const REDIS_PORT = configService.get('REDIS_PORT');
  const REDIS_HOST = configService.get('REDIS_HOST');
  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.REDIS,
    options: {
      retryDelay: 5000,
      retryAttempts: 10000,
      host: REDIS_HOST,
      port: REDIS_PORT,
    },
  });

  await app.startAllMicroservices();
  await app.listen(PORT || 3001, '0.0.0.0');
}
bootstrap();
