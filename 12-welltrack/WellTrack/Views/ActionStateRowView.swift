//
//  ActionStateRowView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import SwiftUI

struct ActionStateRowView: View {
    @Environment(\.managedObjectContext) private var moc
    @ObservedObject var vm: ActionStateViewModel
    
    @State var showingExecutionSheet = false

    var buttonTrigger: TriggerButton? {
        for trigger in vm.actionState.triggers {
            if let trigger = trigger as? TriggerButton {
                return trigger
            }
        }
        return nil
    }

    var hasButtonType: Bool {
        return buttonTrigger != nil
    }
    
    var inputVariableNames: String {
        let names = vm.actionState.inputs.compactMap { ($0 as? Input)?.title }
        return names.joined(separator: ", ")
    }
    
    var body: some View {
        ZStack {
            VStack(alignment: .leading, spacing: 8) {
                Text(vm.actionState.title)
                    .font(.system(size: 26, design: .rounded).bold())
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .overlay(alignment: .topTrailing) {
                if hasButtonType {
                    Button {
                        if let trigger = buttonTrigger {
                            vm.addExecutionRecord(trigger: trigger)
                            showingExecutionSheet = true
                            
                        }
                    } label: {
                        HStack {
                            Image(systemName: buttonTrigger?.systemImage ?? "play.circle.fill")
                        }
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .sheet(isPresented: $vm.showingInputExecutionSheet, content: {
            ExecutingInputView(vm: vm)
        })
//        .sheet(item: $vm.currentExecutionItem,
//               onDismiss: { vm.showingInputSheet = false},
//               content: { NavigationStack { ExecutingInputView()}
//        })

      
    }


}
