using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Game.Collab.Integration;
using Game.Collab.UI;

namespace Game.Collab.Tests.PlayMode
{
    public class DemoFlowTests
    {
        [UnityTest]
        public IEnumerator Damage_UpdatesOverlayAcrossModules()
        {
            var viewGo = new GameObject("test-overlay");
            var bootGo = new GameObject("test-bootstrap");
            try
            {
                var overlay = viewGo.AddComponent<HealthOverlay>();
                var bootstrap = bootGo.AddComponent<DemoBootstrap>();
                bootstrap.SetOverlay(overlay);
                yield return null; // Start()가 실행되도록 한 프레임 대기

                Assert.That(bootstrap.CurrentHp, Is.EqualTo(100));
                bootstrap.TestAttack(15);
                Assert.That(bootstrap.CurrentHp, Is.EqualTo(85));
                Assert.That(overlay.DisplayText, Does.Contain("85/100"));
            }
            finally
            {
                Object.Destroy(viewGo);
                Object.Destroy(bootGo);
            }
        }
    }
}
