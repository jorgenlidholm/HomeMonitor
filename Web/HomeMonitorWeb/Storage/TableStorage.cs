﻿using System.Collections.Generic;
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
            //CloudStorageAccount storageAccount = new CloudStorageAccount(
            //    new Microsoft.WindowsAzure.Storage.Auth.StorageCredentials(
            //    "homemonitorstorage",
            //    "2EUmT/vTMo4hdcp8nXHlnqjUTAzJRNB3IslPqbSKqDjK8EH8CT5t32fHjpkc0hB5eVyexS/D0EBXg4i12D39yg=="), true);

            CloudTableClient tableClient = storageAccount.CreateCloudTableClient();
            _table = tableClient.GetTableReference("SensorMessurement");
            var task = Task.Run(() => { _table.CreateIfNotExistsAsync(); });

            task.Wait();
        }

        public async Task<IEnumerable<SensorMessurement>> Get(int id)
        {
            var operation = new TableQuery<SensorMessurementEntity>()
                .Where(TableQuery.GenerateFilterCondition("PartitionKey", QueryComparisons.Equal, id.ToString()));

            var contiunationToken = new TableContinuationToken();

            var task = await _table.ExecuteQuerySegmentedAsync(operation,contiunationToken);

            return Convert(task.Results);
        }

        private IEnumerable<SensorMessurement> Convert(List<SensorMessurementEntity> results)
        {
            return results.Select(Convert).ToList();
        }

        private SensorMessurement Convert(SensorMessurementEntity results)
        {
            return new SensorMessurement(results.Identity, results.Time, (float) results.Temperature, (float)results.Humidity);
        }

        public async Task Insert(SensorMessurement sensorMessurement)
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
