﻿using System;
using Calcservice;
using Grpc.Core;

namespace PythonService
{
    public interface IPythonBackend
    {
        void Say(string message);
        CalcService.CalcServiceClient Client { get; }
    }

    public class PythonBackend : IPythonBackend
    {
        private Channel _channel;
        public CalcService.CalcServiceClient Client { get; }

        public PythonBackend(string serverAddress = null)
        {
            if (serverAddress is null)
            {
                serverAddress = Environment.GetEnvironmentVariable("PYTHON_BACKEND_ADDR");
            }

            _channel = new Channel(serverAddress, ChannelCredentials.Insecure);
            Client = new CalcService.CalcServiceClient(_channel);
        }

        ~PythonBackend()
        {
            _channel.ShutdownAsync().Wait();
        }

        public void Say(string message)
        {
            var reply = Client.CalcProbability(new CalcRequest {INN = message});
            Console.WriteLine("Greeting: " + reply.Result);
        }
    }
}