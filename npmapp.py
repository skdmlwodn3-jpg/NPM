
import React, { useState } from 'react';
import { IconSparkles, IconScissors, IconMenu, IconFile, IconNote, IconPlus, IconChevronDown, IconChevronUp, IconRobot, IconPalette } from './components/Icons';
import FileSplitter from './components/FileSplitter';
import PersonaGenerator from './components/PersonaGenerator';
import PromptDirector from './components/PromptDirector';
import ImagePromptDirector from './components/ImagePromptDirector';
import { AnalysisStatus, Project, GeneratorState } from './types';

const initialGeneratorState: GeneratorState = {
  status: AnalysisStatus.IDLE, files: [], result: null, error: null, currentFileIndex: -1
};

const defaultProject: Project = {
  id: 'p1', name: '나의 첫 웹소설', createdAt: Date.now(),
  generatorState: { ...initialGeneratorState }, directorSession: []
};

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'splitter'|'generator'|'director'|'image'>('splitter');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [projects, setProjects] = useState<Project[]>([defaultProject]);
  const [activeProjectId, setActiveProjectId] = useState('p1');
  const [newProjectName, setNewProjectName] = useState('');
  const [isProjExpanded, setIsProjExpanded] = useState(false);

  const activeProject = projects.find(p => p.id === activeProjectId) || projects[0];

  const updateProject = (id: string, updates: Partial<Project>) => {
    setProjects(prev => prev.map(p => p.id === id ? { ...p, ...updates } : p));
  };

  const updateGenerator = (newData: Partial<GeneratorState>) => {
    updateProject(activeProjectId, { generatorState: { ...activeProject.generatorState, ...newData } });
  };

  const handleFilesGenerated = (files: File[]) => {
    const processingFiles = files.map(f => ({ file: f, status: 'PENDING' as const }));
    updateGenerator({ files: processingFiles, status: AnalysisStatus.IDLE, result: null, currentFileIndex: -1 });
    setActiveTab('generator');
  };

  const createProject = () => {
    if (!newProjectName.trim()) return;
    const newP: Project = {
      id: Date.now().toString(), name: newProjectName, createdAt: Date.now(),
      generatorState: { ...initialGeneratorState }, directorSession: []
    };
    setProjects(p => [...p, newP]);
    setActiveProjectId(newP.id);
    setNewProjectName('');
    setIsProjExpanded(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans flex flex-col lg:flex-row">
      {/* Mobile Header */}
      <div className="lg:hidden bg-slate-900 border-b border-slate-800 p-4 flex justify-between items-center sticky top-0 z-50">
        <span className="font-bold text-white flex items-center gap-2"><IconNote /> Novelpia Maker</span>
        <button onClick={() => setSidebarOpen(!sidebarOpen)}><IconMenu /></button>
      </div>

      {/* Sidebar - Widened to 350px */}
      <aside className={`fixed lg:sticky top-0 h-screen w-[350px] bg-slate-900 border-r border-slate-800 z-40 transition-transform duration-300 flex flex-col ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
        <div className="p-6 h-full flex flex-col overflow-y-auto custom-scrollbar">
          <div className="hidden lg:flex items-center gap-3 mb-8">
            <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg"><IconNote /></div>
            <h1 className="font-bold text-lg text-white leading-tight">Novelpia<br/>Prompt Maker</h1>
          </div>

          <div className="mb-6">
            <div className="relative">
              <select value={activeProjectId} onChange={e => setActiveProjectId(e.target.value)} 
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white focus:ring-2 focus:ring-indigo-500 appearance-none cursor-pointer">
                {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
              </select>
              <div className="absolute right-3 top-3.5 pointer-events-none text-slate-400"><IconChevronDown /></div>
            </div>
            
            <div className="mt-2">
              <button onClick={() => setIsProjExpanded(!isProjExpanded)} className="flex items-center justify-between w-full text-xs text-indigo-400 font-bold py-1">
                <span className="flex items-center gap-1"><IconPlus /> 새 프로젝트</span>
                {isProjExpanded ? <IconChevronUp /> : <IconChevronDown />}
              </button>
              {isProjExpanded && (
                <div className="mt-2 bg-slate-800/50 p-2 rounded border border-slate-700/50 animate-fade-in">
                  <input value={newProjectName} onChange={e => setNewProjectName(e.target.value)} placeholder="프로젝트명" className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs mb-2 text-white" />
                  <button onClick={createProject} className="w-full bg-indigo-600 text-white text-xs py-1 rounded font-bold">생성</button>
                </div>
              )}
            </div>
          </div>

          <nav className="space-y-2 flex-1">
             {[
               { id: 'splitter', label: '파일 전처리 도구', icon: <IconScissors />, color: 'bg-indigo-500' },
               { id: 'generator', label: '스토리/캐릭터 분석기', icon: <IconSparkles />, color: 'bg-indigo-500' },
               { id: 'director', label: '프롬프트 디렉터', icon: <IconRobot />, color: 'bg-pink-500' },
               { id: 'image', label: '이미지 프롬프트', icon: <IconPalette />, color: 'bg-green-500' }
             ].map((item) => (
               <button key={item.id} onClick={() => { setActiveTab(item.id as any); setSidebarOpen(false); }}
                 className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                   activeTab === item.id ? 'bg-slate-800 text-white border border-slate-700 shadow-lg' : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'
                 }`}>
                 <div className={`p-1.5 rounded-md ${activeTab === item.id ? `${item.color} text-white` : 'bg-slate-800 text-slate-500'}`}>{item.icon}</div>
                 {item.label}
               </button>
             ))}
          </nav>

          <div className="mt-8 pt-6 border-t border-slate-800 text-xs text-slate-500">
             <p className="flex items-center gap-2 mb-2"><span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]"></span> Gemini 3 Flash Ready</p>
             <p>© 2024 Novelpia Prompt Maker</p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 min-w-0 bg-slate-950 pt-[80px] lg:pt-0">
        <div className="max-w-7xl mx-auto px-4 lg:px-8 py-12">
           <div className="mb-8 flex justify-between items-end border-b border-slate-800 pb-6">
             <div>
               <div className="flex items-center gap-2 mb-1">
                 <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                   activeTab === 'director' ? 'bg-pink-900/50 text-pink-300 border-pink-500/30' : 
                   activeTab === 'image' ? 'bg-green-900/50 text-green-300 border-green-500/30' : 
                   'bg-indigo-900/50 text-indigo-300 border-indigo-500/30'
                 }`}>STEP {activeTab === 'image' ? 'EXTRA' : activeTab === 'splitter' ? '01' : activeTab === 'generator' ? '02' : '03'}</span>
                 <h1 className="text-2xl font-bold text-white">
                   {activeTab === 'splitter' ? '파일 전처리 도구' : 
                    activeTab === 'generator' ? '스토리/캐릭터 분석기' : 
                    activeTab === 'director' ? '프롬프트 디렉터' : '이미지 프롬프트'}
                 </h1>
               </div>
               <p className="text-slate-400 text-sm">
                 {activeTab === 'splitter' ? '대용량 텍스트를 안전하게 분할합니다.' : 
                  activeTab === 'generator' ? '캐릭터와 서사를 심층 분석합니다.' : 
                  activeTab === 'director' ? 'AI와 대화하며 프롬프트를 완성합니다.' : '캐릭터 외형 태그를 생성합니다.'}
               </p>
             </div>
             <div className="hidden md:block text-right">
               <p className="text-[10px] uppercase text-slate-500 font-bold">Current Project</p>
               <p className="text-white font-bold">{activeProject.name}</p>
             </div>
           </div>

           <div key={activeProject.id} className="animate-fade-in">
             {activeTab === 'splitter' && <FileSplitter projectName={activeProject.name} onFilesGenerated={handleFilesGenerated} />}
             {activeTab === 'generator' && <PersonaGenerator projectName={activeProject.name} data={activeProject.generatorState} onUpdate={updateGenerator} />}
             {activeTab === 'director' && <PromptDirector projectName={activeProject.name} masterJson={activeProject.generatorState.result} history={activeProject.directorSession} onUpdateHistory={h => updateProject(activeProjectId, { directorSession: h })} />}
             {activeTab === 'image' && <ImagePromptDirector projectName={activeProject.name} masterJson={activeProject.generatorState.result} />}
           </div>
        </div>
      </main>

      {sidebarOpen && <div className="fixed inset-0 bg-black/50 z-30 lg:hidden backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        @keyframes fade-in-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .animate-fade-in-up { animation: fade-in-up 0.5s ease-out forwards; }
      `}</style>
    </div>
  );
};

export default App;
