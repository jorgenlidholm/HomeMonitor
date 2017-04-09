using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using HomeMonitor.Library;

namespace HomeMonitor.Tests
{
    [TestClass]
    public class AuthenticationTests
    {
        [TestMethod]
        public void GetAuthenticationTokenShouldReturnByteArray()
        {
            var sut = new Authentication();
            Assert.IsNotNull(sut.GetAuthenticationToken("Hello World"));
        }

        [TestMethod]
        public void ValidateShouldReturnTrue()
        {
            var key = "56f6f3af595eefd5953b47b6ac1b7ccfda6a1fa3dbde374bf3f0429f992eddbf";
            var sut = new Authentication();
            Assert.IsTrue(sut.ValidateAuthenticationToken(key, "Hello World"));
        }
    }
}
