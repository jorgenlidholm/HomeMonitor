using System.Collections.Generic;
using System.Text;
using System.Linq;
using HomeMonitorWeb.Contracts;
using Microsoft.WindowsAzure.Storage; // Namespace for CloudStorageAccount
using Microsoft.WindowsAzure.Storage.Table; // Namespace for Table storage types
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;
using System;

namespace HomeMonitorWeb.Storage
{
    public class TableStorage
    {
        CloudTable _table;
        public TableStorage(IOptions<SensorMessurementOptions> configuration)
        {
            var connectionString = configuration.Value.StorageConnectionString;
            CloudStorageAccount storageAccount = CloudStorageAccount.Parse(connectionString);

            CloudTableClient tableClient = storageAccount.CreateCloudTableClient();
            _table = tableClient.GetTableReference("SensorMessurement2");
            var task = Task.Run(() => { _table.CreateIfNotExistsAsync(); });

            task.Wait();
        }

        internal async Task<int[]> GetSensorIds()
        {
            return new int[]{ 21, 135 };
        }

        public async Task<IEnumerable<SensorMessurement>> Get(int id)
        {
            var operation = new TableQuery<SensorMessurementEntity>()
                .Where(TableQuery.GenerateFilterCondition("PartitionKey", QueryComparisons.Equal, id.ToString()));

            List<SensorMessurementEntity> list = new List<SensorMessurementEntity>();
            var contiunationToken = new TableContinuationToken();

            do
            {
                var task = await _table.ExecuteQuerySegmentedAsync(operation, contiunationToken);
                if(task.Results != null)
                    list.AddRange(task.Results);
                contiunationToken = task.ContinuationToken;
            }
            while (contiunationToken != null);



            return Convert(list);
        }

        private IEnumerable<SensorMessurement> Convert(List<SensorMessurementEntity> results)
        {
            return results.Select(Convert).ToList();
        }

        private SensorMessurement Convert(SensorMessurementEntity results)
        {
            return new SensorMessurement(results.Identity, results.Time, (float) results.Temperature, (float)results.Humidity);
        }

        public async Task Insert(IEnumerable<SensorMessurement> sensorMessurements)
        {

            foreach (var sensorMessurement in sensorMessurements)
            {
                var operation = TableOperation.Insert(new SensorMessurementEntity(sensorMessurement.Identity, sensorMessurement.Time)
                {
                    Temperature = sensorMessurement.Temperature,
                    Humidity = sensorMessurement.Humidity
                });

                await _table.ExecuteAsync(operation);
            }
        }
    }
}
