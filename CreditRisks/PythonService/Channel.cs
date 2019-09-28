using System;
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

        public PythonBackend()
        {
            _channel = new Channel("127.0.0.1:50051", ChannelCredentials.Insecure);
            Client = new CalcService.CalcServiceClient(_channel);
        }

        ~PythonBackend()
        {
            _channel.ShutdownAsync().Wait();
        }

        public void Say(string message)
        {
            var reply = Client.CalcProbability(new CalcRequest {INN = message, Algorithm = AlgorithmType.DefaultHand});
            Console.WriteLine("Greeting: " + reply.Probability);
        }
    }
}