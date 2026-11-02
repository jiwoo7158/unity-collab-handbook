using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using Game.Collab.Integration;
using Game.Collab.UI;

namespace Game.Collab.Editor
{
    public static class CreateDemoScene
    {
        [MenuItem("Tools/Collaboration Lab/Create Demo Scene")]
        public static void Create()
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var overlayObject = new GameObject("HealthOverlay");
            var overlay = overlayObject.AddComponent<HealthOverlay>();
            var bootstrapObject = new GameObject("CombatBootstrap");
            var bootstrap = bootstrapObject.AddComponent<DemoBootstrap>();
            bootstrap.SetOverlay(overlay);

            const string folder = "Assets/_Game/Demo";
            Directory.CreateDirectory(folder);
            EditorSceneManager.SaveScene(scene, folder + "/CollaborationDemo.unity");
            AssetDatabase.Refresh();
            Debug.Log("Demo created: Assets/_Game/Demo/CollaborationDemo.unity");
        }
    }
}
